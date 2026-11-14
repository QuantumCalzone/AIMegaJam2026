#include "Actors/StageActorCharacter.h"
#include "Actors/ActorBrainComponent.h"
#include "AI/BarkSubsystem.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Animation/AnimationAsset.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "PhysicsEngine/BodyInstance.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "AIController.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "Take37.h"

namespace
{
	const FVector StageExit(-1250.0, -300.0, 0.0);
}

AStageActorCharacter::AStageActorCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	AIControllerClass = AAIController::StaticClass();
	bUseControllerRotationYaw = false;

	GetCapsuleComponent()->InitCapsuleSize(34.f, 90.f);
	UCharacterMovementComponent* Move = GetCharacterMovement();
	Move->bOrientRotationToMovement = true;
	Move->RotationRate = FRotator(0.f, 540.f, 0.f);
	Move->MaxWalkSpeed = 140.f;
	Move->bEnablePhysicsInteraction = true;

	USkeletalMeshComponent* M = GetMesh();
	M->SetRelativeLocation(FVector(0.f, 0.f, -90.f));
	M->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	M->SetAnimationMode(EAnimationMode::AnimationSingleNode);
}

void AStageActorCharacter::Setup(const FStageActorSpec& InSpec)
{
	Spec = InSpec;
	DisplayName = Spec.Name;
	Role = Spec.Role;
	StartTransform = GetActorTransform();
	SetActorScale3D(FVector(Spec.Scale));

	USkeletalMeshComponent* M = GetMesh();
	if (USkeletalMesh* Skel = LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/Character/Mesh/SK_Mannequin.SK_Mannequin")))
	{
		M->SetSkeletalMesh(Skel);
	}
	else
	{
		UE_LOG(LogTake37, Warning, TEXT("Mannequin mesh missing; %s will be invisible."), *Spec.Name);
	}
	IdleAnim = LoadObject<UAnimationAsset>(nullptr, TEXT("/Game/Animations/ThirdPersonIdle.ThirdPersonIdle"));
	WalkAnim = LoadObject<UAnimationAsset>(nullptr, TEXT("/Game/Animations/ThirdPersonWalk.ThirdPersonWalk"));
	RunAnim = LoadObject<UAnimationAsset>(nullptr, TEXT("/Game/Animations/ThirdPersonRun.ThirdPersonRun"));
	HopAnim = LoadObject<UAnimationAsset>(nullptr, TEXT("/Game/Animations/ThirdPersonJump_Start.ThirdPersonJump_Start"));

	// Flat character colour on the mannequin body.
	if (UMaterialInterface* Base = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Materials/M_Greybox.M_Greybox")))
	{
		for (int32 i = 0; i < M->GetNumMaterials(); ++i)
		{
			UMaterialInstanceDynamic* MID = UMaterialInstanceDynamic::Create(Base, this);
			MID->SetVectorParameterValue(TEXT("Color"), Spec.Color);
			MID->SetScalarParameterValue(TEXT("Roughness"), 0.6f);
			M->SetMaterial(i, MID);
		}
	}

	// Ragdoll collisions must reach the chain system so what an actor knocks over scores as IMPROV.
	M->SetNotifyRigidBodyCollision(true);
	M->OnComponentHit.AddUniqueDynamic(this, &AStageActorCharacter::OnMeshHit);

	ChainProp = NewObject<UChainPropComponent>(this, TEXT("ChainProp"));
	ChainProp->Category = EChainCategory::Actor;
	ChainProp->DisplayName = Spec.Name;
	ChainProp->BaseValue = 500.f;
	ChainProp->MinImpulseToCount = 300.f;
	ChainProp->RegisterComponent();

	Brain = NewObject<UActorBrainComponent>(this, TEXT("Brain"));
	Brain->Traits = Spec.Traits;
	Brain->RegisterComponent();

	BuildCostume();
	UpdateAnimation(0.f);
}

void AStageActorCharacter::BuildCostume()
{
	USkeletalMeshComponent* M = GetMesh();
	UCapsuleComponent* Cap = GetCapsuleComponent();
	auto Sph = [&](FName Bone, FVector Off, FVector D, FLinearColor C, float Em = 0.f)
	{
		return Take37Visuals::Add(this, M, Parts, TEXT("Sphere"), Off, D, C, FRotator::ZeroRotator, Em, 0.5f, 0.f, Bone);
	};
	auto Cyl = [&](FName Bone, FVector Off, FVector D, FLinearColor C, FRotator R = FRotator::ZeroRotator, float Em = 0.f)
	{
		return Take37Visuals::Add(this, M, Parts, TEXT("Cylinder"), Off, D, C, R, Em, 0.5f, 0.f, Bone);
	};
	auto Box = [&](FName Bone, FVector Off, FVector D, FLinearColor C, FRotator R = FRotator::ZeroRotator, float Em = 0.f)
	{
		return Take37Visuals::Add(this, M, Parts, TEXT("Cube"), Off, D, C, R, Em, 0.5f, 0.f, Bone);
	};

	const FName Head(TEXT("head"));
	const FLinearColor White(0.97f, 0.97f, 0.95f);
	const FLinearColor Black(0.03f, 0.03f, 0.04f);

	// Face: skin-toned head with big cartoon eyes. Bone X runs up the head on the mannequin skeleton.
	Sph(Head, FVector(11, 0, 0), FVector(26, 24, 29), Spec.Skin);
	for (int32 s : { -1, 1 })
	{
		Sph(Head, FVector(13, s * 5.2f, 10.5f), FVector(7, 5, 7), White);
		Sph(Head, FVector(13, s * 5.2f, 12.8f), FVector(3.2f, 2.5f, 3.2f), Black);
	}
	Sph(Head, FVector(8, 0, 12.5f), FVector(4, 4, 4), FLinearColor(Spec.Skin.R * 0.9f, Spec.Skin.G * 0.7f, Spec.Skin.B * 0.65f));
	Sph(TEXT("hand_r"), FVector(7, 0, 0), FVector(12, 10, 12), Spec.Skin);
	Sph(TEXT("hand_l"), FVector(7, 0, 0), FVector(12, 10, 12), Spec.Skin);
	Sph(TEXT("foot_r"), FVector(2, 0, 0), FVector(14, 10, 24), FLinearColor(0.2f, 0.12f, 0.08f));
	Sph(TEXT("foot_l"), FVector(2, 0, 0), FVector(14, 10, 24), FLinearColor(0.2f, 0.12f, 0.08f));

	if (Spec.Id == TEXT("brick"))
	{
		Cyl(Head, FVector(21, 0, 0), FVector(50, 50, 2.5f), FLinearColor(0.95f, 0.86f, 0.62f));
		Cyl(Head, FVector(27, 0, 0), FVector(27, 27, 13), FLinearColor(0.95f, 0.86f, 0.62f));
		Cyl(Head, FVector(23.5f, 0, 0), FVector(28, 28, 3), FLinearColor(0.35f, 0.15f, 0.08f));
		Sph(TEXT("neck_01"), FVector(0, 0, 0), FVector(22, 22, 12), FLinearColor(0.9f, 0.1f, 0.1f));
		Sph(TEXT("spine_03"), FVector(0, 9, 0), FVector(7, 4, 7), FLinearColor(1.f, 0.8f, 0.1f), 2.f);
	}
	else if (Spec.Id == TEXT("vivienne"))
	{
		Sph(Head, FVector(22, 0, 0), FVector(24, 22, 34), FLinearColor(0.82f, 0.85f, 0.9f));
		Sph(Head, FVector(34, 0, 0), FVector(14, 14, 14), FLinearColor(0.82f, 0.85f, 0.9f));
		for (int32 i = 0; i < 9; ++i)
		{
			const float A = i * 40.f * PI / 180.f;
			Sph(TEXT("neck_01"), FVector(-2, FMath::Cos(A) * 11.f, FMath::Sin(A) * 11.f), FVector(11, 10, 10), FLinearColor(1.f, 0.2f, 0.65f));
		}
		// Gown hangs on the capsule so it hides the legs; it is hidden while she is ragdolled.
		SkirtParts.Add(Take37Visuals::Add(this, Cap, Parts, TEXT("Cone"), FVector(0, 0, -30), FVector(86, 86, 120), Spec.Color, FRotator::ZeroRotator, 0.1f, 0.4f, 0.2f));
		SkirtParts.Add(Take37Visuals::Add(this, Cap, Parts, TEXT("Cylinder"), FVector(0, 0, 28), FVector(40, 40, 26), Spec.Color, FRotator::ZeroRotator, 0.1f, 0.4f, 0.2f));
	}
	else if (Spec.Id == TEXT("gus"))
	{
		Sph(Head, FVector(21, 0, 0), FVector(29, 27, 17), FLinearColor(0.1f, 0.65f, 0.3f));
		Sph(Head, FVector(29, 0, 0), FVector(7, 7, 7), FLinearColor(0.1f, 0.65f, 0.3f));
		for (int32 s : { -1, 1 })
		{
			Cyl(Head, FVector(9, s * 13.5f, 0), FVector(11, 11, 6), Black, FRotator(0, 0, 90));
		}
		Cyl(Head, FVector(19, 0, 0), FVector(2, 29, 2), Black, FRotator(90, 0, 0));
		Box(TEXT("hand_l"), FVector(8, 0, 0), FVector(30, 3, 22), FLinearColor(0.75f, 0.55f, 0.3f));
		Box(TEXT("spine_03"), FVector(0, 9, 0), FVector(5, 3, 8), FLinearColor(0.9f, 0.9f, 0.95f));
	}
}

void AStageActorCharacter::SetSkirtVisible(bool bVisible)
{
	for (UStaticMeshComponent* S : SkirtParts)
	{
		if (S)
		{
			S->SetVisibility(bVisible);
		}
	}
}

void AStageActorCharacter::Bark(const TCHAR* Tag, int32 MinIntensity)
{
	if (UBarkSubsystem* B = GetWorld()->GetSubsystem<UBarkSubsystem>())
	{
		B->RequestBark(FName(*Spec.BarkId), FName(Tag), MinIntensity);
	}
}

// ----------------------------------------------------------------------------- route and states

void AStageActorCharacter::StartRoute()
{
	StepIndex = 0;
	if (Brain)
	{
		Brain->Reset();
	}
	State = Spec.Route.Num() > 0 ? EState::Moving : EState::Done;
}

void AStageActorCharacter::ForceStand(const FVector& Location)
{
	USkeletalMeshComponent* M = GetMesh();
	M->SetSimulatePhysics(false);
	M->SetCollisionProfileName(TEXT("CharacterMesh"));
	M->AttachToComponent(GetCapsuleComponent(), FAttachmentTransformRules::SnapToTargetNotIncludingScale);
	M->SetRelativeLocation(FVector(0.f, 0.f, -90.f));
	M->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	M->SetNotifyRigidBodyCollision(true);
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	GetCapsuleComponent()->SetWorldLocation(Location);
	GetCapsuleComponent()->SetWorldRotation(FRotator(0.f, GetActorRotation().Yaw, 0.f));
	GetCharacterMovement()->SetMovementMode(MOVE_Walking);
	SetSkirtVisible(true);
	SetActorHiddenInGame(false);
	CurrentAnim = -1;
}

void AStageActorCharacter::ResetToStart()
{
	State = EState::Idle;
	Action = EAction::None;
	StepIndex = 0;
	ForceStand(StartTransform.GetLocation());
	SetActorTransform(StartTransform, false, nullptr, ETeleportType::TeleportPhysics);
	GetCharacterMovement()->StopMovementImmediately();
	if (Brain)
	{
		Brain->Reset();
	}
	UpdateAnimation(0.f);
}

void AStageActorCharacter::EndAction()
{
	Action = EAction::None;
	State = ReturnState;
	CurrentAnim = -1;
}

void AStageActorCharacter::GetUp()
{
	const FVector Pelvis = GetMesh()->GetBoneLocation(TEXT("pelvis"));
	ForceStand(Pelvis + FVector(0.0, 0.0, 90.0 * Spec.Scale));
	State = Spec.Route.IsValidIndex(StepIndex) ? EState::Moving : EState::Done;
	if (Brain && Brain->Composure > 0.4f)
	{
		Bark(TEXT("Relief"));
	}
}

// ----------------------------------------------------------------------------- actions

void AStageActorCharacter::DoFace(const FVector& Target)
{
	FVector To = Target - GetActorLocation();
	To.Z = 0.0;
	if (!To.IsNearlyZero())
	{
		SetActorRotation(FRotator(0.f, To.Rotation().Yaw, 0.f));
	}
}

void AStageActorCharacter::DoHop()
{
	if (IsBusy())
	{
		return;
	}
	ReturnState = State;
	State = EState::Acting;
	Action = EAction::Hop;
	ActionTimer = 0.7f;
	GetCharacterMovement()->StopMovementImmediately();
	if (HopAnim)
	{
		GetMesh()->PlayAnimation(HopAnim, false);
	}
	CurrentAnim = -2;
}

void AStageActorCharacter::DoRecoil(const FVector& AwayFrom, float Duration)
{
	if (State == EState::Down || State == EState::Out)
	{
		return;
	}
	if (State != EState::Acting)
	{
		ReturnState = State;
	}
	State = EState::Acting;
	Action = EAction::Recoil;
	ActionTimer = Duration;
	ActionDir = (GetActorLocation() - AwayFrom).GetSafeNormal2D();
	GetCharacterMovement()->MaxWalkSpeed = 260.f;
}

void AStageActorCharacter::DoPanicRun(float Duration)
{
	if (State == EState::Down || State == EState::Out)
	{
		return;
	}
	if (State != EState::Acting)
	{
		ReturnState = State;
	}
	State = EState::Acting;
	Action = EAction::Panic;
	ActionTimer = Duration;
	PanicRedirect = 0.f;
	GetCharacterMovement()->MaxWalkSpeed = 380.f;
}

void AStageActorCharacter::DoPose(float Duration)
{
	if (IsBusy())
	{
		return;
	}
	ReturnState = State;
	State = EState::Acting;
	Action = EAction::Pose;
	ActionTimer = Duration;
	GetCharacterMovement()->StopMovementImmediately();
}

void AStageActorCharacter::DoDive(const FVector& Target)
{
	if (State == EState::Down || State == EState::Out)
	{
		return;
	}
	if (State != EState::Acting)
	{
		ReturnState = State;
	}
	FVector To = Target - GetActorLocation();
	To.Z = 0.0;
	const FVector Dir = To.GetSafeNormal();
	SetActorRotation(FRotator(0.f, Dir.Rotation().Yaw, 0.f));
	State = EState::Acting;
	Action = EAction::Dive;
	ActionTimer = 0.55f;
	ActionDir = Dir;
	LaunchCharacter(Dir * 900.f + FVector(0, 0, 320.f), true, true);
	if (HopAnim)
	{
		GetMesh()->PlayAnimation(HopAnim, false);
	}
	CurrentAnim = -2;
}

void AStageActorCharacter::DoShove(AStageActorCharacter* Target)
{
	if (!Target || State == EState::Down || State == EState::Out)
	{
		return;
	}
	if (State != EState::Acting)
	{
		ReturnState = State;
	}
	State = EState::Acting;
	Action = EAction::Shove;
	ActionTimer = 6.f;
	ShoveTarget = Target;
	GetCharacterMovement()->MaxWalkSpeed = 330.f;
}

void AStageActorCharacter::DoStormOff()
{
	if (State == EState::Down || State == EState::Out)
	{
		return;
	}
	State = EState::Acting;
	Action = EAction::StormOff;
	ActionTimer = 20.f;
	GetCharacterMovement()->MaxWalkSpeed = 240.f;
}

void AStageActorCharacter::DoRagdoll(const FVector& VelocityChange)
{
	if (State == EState::Down || State == EState::Out)
	{
		return;
	}
	State = EState::Down;
	Action = EAction::None;
	DownTime = 0.f;
	CalmTime = 0.f;

	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GetCharacterMovement()->DisableMovement();
	GetCharacterMovement()->StopMovementImmediately();
	SetSkirtVisible(false);

	USkeletalMeshComponent* M = GetMesh();
	M->SetCollisionProfileName(TEXT("Ragdoll"));
	M->SetAllBodiesSimulatePhysics(true);
	M->SetSimulatePhysics(true);
	M->WakeAllRigidBodies();
	M->SetNotifyRigidBodyCollision(true);
	// Keep it readable: damp spinning so ragdolls do not flop like noodles (GDD section 9.3).
	for (FBodyInstance* B : M->Bodies)
	{
		if (B)
		{
			B->LinearDamping = 0.1f;
			B->AngularDamping = 1.5f;
			B->UpdateDampingProperties();
		}
	}
	M->AddImpulse(VelocityChange, TEXT("pelvis"), true);
}

void AStageActorCharacter::OnMeshHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
	if (State != EState::Down || !OtherActor || !ChainProp)
	{
		return;
	}
	UChainPropComponent* Other = OtherActor->FindComponentByClass<UChainPropComponent>();
	if (!Other || Other == ChainProp)
	{
		return;
	}
	if (UChainReactionSubsystem* Sub = GetWorld()->GetSubsystem<UChainReactionSubsystem>())
	{
		// Refresh the window so a long tumble keeps crediting what it hits.
		ChainProp->LastCreditTime = GetWorld()->GetTimeSeconds();
		Sub->ReportHit(ChainProp, Other, FMath::Max(NormalImpulse.Size(), 2000.f), Hit.ImpactPoint);
	}
}

// ----------------------------------------------------------------------------- tick

void AStageActorCharacter::UpdateAnimation(float Speed)
{
	if (State == EState::Down || (State == EState::Acting && (Action == EAction::Hop || Action == EAction::Dive)))
	{
		return;
	}
	int32 Want = 0;
	if (Speed > 220.f)
	{
		Want = 2;
	}
	else if (Speed > 12.f)
	{
		Want = 1;
	}
	UAnimationAsset* Asset = (Want == 2) ? RunAnim.Get() : (Want == 1 ? WalkAnim.Get() : IdleAnim.Get());
	USkeletalMeshComponent* M = GetMesh();
	if (Want != CurrentAnim && Asset)
	{
		CurrentAnim = Want;
		M->PlayAnimation(Asset, true);
	}
	// Match stride to ground speed so feet do not skate.
	const float Rate = (Want == 1) ? FMath::Clamp(Speed / 140.f, 0.6f, 1.6f) : (Want == 2 ? FMath::Clamp(Speed / 330.f, 0.7f, 1.5f) : 1.f);
	M->SetPlayRate(Rate);
}

void AStageActorCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	const FVector Loc = GetActorLocation();

	switch (State)
	{
	case EState::Moving:
		if (Spec.Route.IsValidIndex(StepIndex))
		{
			const FRouteStep& Step = Spec.Route[StepIndex];
			FVector To = Step.Mark - Loc;
			To.Z = 0.0;
			if (To.Size() < 45.0)
			{
				State = EState::Waiting;
				WaitTimer = Step.Wait;
			}
			else
			{
				GetCharacterMovement()->MaxWalkSpeed = Step.Speed;
				AddMovementInput(To.GetSafeNormal(), 1.f);
			}
		}
		break;

	case EState::Waiting:
		WaitTimer -= DeltaTime;
		if (WaitTimer <= 0.f)
		{
			++StepIndex;
			State = Spec.Route.IsValidIndex(StepIndex) ? EState::Moving : EState::Done;
		}
		break;

	case EState::Acting:
		ActionTimer -= DeltaTime;
		switch (Action)
		{
		case EAction::Recoil:
			AddMovementInput(ActionDir, 1.f);
			break;
		case EAction::Panic:
			PanicRedirect -= DeltaTime;
			if (PanicRedirect <= 0.f)
			{
				PanicRedirect = 0.7f;
				ActionDir = FVector(FMath::FRandRange(-1.f, 1.f), FMath::FRandRange(-1.f, 1.f), 0.f).GetSafeNormal();
			}
			AddMovementInput(ActionDir, 1.f);
			break;
		case EAction::Dive:
			if (ActionTimer <= 0.f)
			{
				DoRagdoll(ActionDir * 420.f + FVector(0, 0, 120.f));
				return;
			}
			break;
		case EAction::Shove:
			if (AStageActorCharacter* T = ShoveTarget.Get())
			{
				FVector To = T->GetActorLocation() - Loc;
				To.Z = 0.0;
				if (To.Size() < 170.0)
				{
					T->Bark(TEXT("Hurt_Light"));
					T->DoRagdoll(To.GetSafeNormal() * 520.f + FVector(0, 0, 220.f));
					Bark(TEXT("Relief"));
					EndAction();
				}
				else
				{
					AddMovementInput(To.GetSafeNormal(), 1.f);
				}
			}
			else
			{
				EndAction();
			}
			break;
		case EAction::StormOff:
		{
			FVector To = StageExit - Loc;
			To.Z = 0.0;
			if (To.Size() < 90.0)
			{
				State = EState::Out;
				Action = EAction::None;
				SetActorHiddenInGame(true);
				GetCharacterMovement()->StopMovementImmediately();
				return;
			}
			AddMovementInput(To.GetSafeNormal(), 1.f);
			break;
		}
		default:
			break;
		}
		if (State == EState::Acting && ActionTimer <= 0.f && Action != EAction::StormOff)
		{
			EndAction();
		}
		break;

	case EState::Down:
	{
		DownTime += DeltaTime;
		USkeletalMeshComponent* M = GetMesh();
		const FVector Vel = M->GetPhysicsLinearVelocity(TEXT("pelvis"));
		CalmTime = (Vel.Size() < 20.f) ? CalmTime + DeltaTime : 0.f;
		if (DownTime > 1.2f && (CalmTime > 0.5f || DownTime > 6.f))
		{
			GetUp();
		}
		return;
	}
	default:
		break;
	}

	UpdateAnimation(GetVelocity().Size2D());
}
