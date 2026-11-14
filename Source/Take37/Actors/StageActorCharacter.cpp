#include "Actors/StageActorCharacter.h"
#include "Chain/ChainPropComponent.h"
#include "Animation/AnimationAsset.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "AIController.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "Take37.h"

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

	ChainProp = NewObject<UChainPropComponent>(this, TEXT("ChainProp"));
	ChainProp->Category = EChainCategory::Actor;
	ChainProp->DisplayName = Spec.Name;
	ChainProp->BaseValue = 500.f;
	ChainProp->MinImpulseToCount = 300.f;
	ChainProp->RegisterComponent();

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
	// Hands
	Sph(TEXT("hand_r"), FVector(7, 0, 0), FVector(12, 10, 12), Spec.Skin);
	Sph(TEXT("hand_l"), FVector(7, 0, 0), FVector(12, 10, 12), Spec.Skin);
	// Shoes
	Sph(TEXT("foot_r"), FVector(2, 0, 0), FVector(14, 10, 24), FLinearColor(0.2f, 0.12f, 0.08f));
	Sph(TEXT("foot_l"), FVector(2, 0, 0), FVector(14, 10, 24), FLinearColor(0.2f, 0.12f, 0.08f));

	if (Spec.Id == TEXT("brick"))
	{
		Cyl(Head, FVector(21, 0, 0), FVector(50, 50, 2.5f), FLinearColor(0.95f, 0.86f, 0.62f));
		Cyl(Head, FVector(27, 0, 0), FVector(27, 27, 13), FLinearColor(0.95f, 0.86f, 0.62f));
		Cyl(Head, FVector(23.5f, 0, 0), FVector(28, 28, 3), FLinearColor(0.35f, 0.15f, 0.08f));
		Sph(TEXT("neck_01"), FVector(0, 0, 0), FVector(22, 22, 12), FLinearColor(0.9f, 0.1f, 0.1f));
		Sph(TEXT("spine_03"), FVector(0, 9, 0), FVector(7, 4, 7), FLinearColor(1.f, 0.8f, 0.1f), 2.f);
		Sph(Head, FVector(5, 0, -5), FVector(8, 16, 4), FLinearColor(0.15f, 0.07f, 0.04f));   // chin-strap shadow reads as stubble
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
		// Gown: attached to the capsule so it hides the legs and doesn't swing wildly.
		Take37Visuals::Add(this, Cap, Parts, TEXT("Cone"), FVector(0, 0, -30), FVector(86, 86, 120), Spec.Color, FRotator::ZeroRotator, 0.1f, 0.4f, 0.2f);
		Take37Visuals::Add(this, Cap, Parts, TEXT("Cylinder"), FVector(0, 0, 28), FVector(40, 40, 26), Spec.Color, FRotator::ZeroRotator, 0.1f, 0.4f, 0.2f);
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

void AStageActorCharacter::StartRoute()
{
	StepIndex = 0;
	if (Spec.Route.Num() == 0)
	{
		State = EState::Done;
		return;
	}
	State = EState::Moving;
}

void AStageActorCharacter::ResetToStart()
{
	State = EState::Idle;
	StepIndex = 0;
	SetActorTransform(StartTransform, false, nullptr, ETeleportType::TeleportPhysics);
	GetCharacterMovement()->StopMovementImmediately();
	UpdateAnimation(0.f);
}

void AStageActorCharacter::UpdateAnimation(float Speed)
{
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

	if (State == EState::Moving && Spec.Route.IsValidIndex(StepIndex))
	{
		const FRouteStep& Step = Spec.Route[StepIndex];
		FVector To = Step.Mark - GetActorLocation();
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
	else if (State == EState::Waiting)
	{
		WaitTimer -= DeltaTime;
		if (WaitTimer <= 0.f)
		{
			++StepIndex;
			State = Spec.Route.IsValidIndex(StepIndex) ? EState::Moving : EState::Done;
		}
	}

	UpdateAnimation(GetVelocity().Size2D());
}
