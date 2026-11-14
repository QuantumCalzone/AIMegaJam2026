#include "Player/DirectorPawn.h"
#include "Player/PlacementComponent.h"
#include "Chain/CueDeviceActor.h"
#include "Core/Take37Types.h"
#include "Core/TakeDirectorSubsystem.h"
#include "UI/Take37HUD.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "InputModifiers.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "Take37.h"

ADirectorPawn::ADirectorPawn()
{
	PrimaryActorTick.bCanEverTick = true;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	Arm = CreateDefaultSubobject<USpringArmComponent>(TEXT("Arm"));
	Arm->SetupAttachment(Root);
	Arm->bDoCollisionTest = false;
	Arm->bUsePawnControlRotation = false;
	Arm->SetUsingAbsoluteRotation(true);
	Arm->bEnableCameraLag = true;
	Arm->CameraLagSpeed = 12.f;

	Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
	Camera->SetupAttachment(Arm, USpringArmComponent::SocketName);
	Camera->FieldOfView = 60.f;

	Placement = CreateDefaultSubobject<UPlacementComponent>(TEXT("Placement"));

	AutoPossessPlayer = EAutoReceiveInput::Player0;
}

void ADirectorPawn::BeginPlay()
{
	Super::BeginPlay();
	SetActorLocation(Pivot);
}

void ADirectorPawn::BuildInput()
{
	if (Context)
	{
		return;
	}
	Context = NewObject<UInputMappingContext>(this, TEXT("IMC_Director"));

	auto MakeAction = [this](const TCHAR* Name, EInputActionValueType Type)
	{
		UInputAction* A = NewObject<UInputAction>(this, Name);
		A->ValueType = Type;
		return A;
	};
	auto Negate = [this]() { return NewObject<UInputModifierNegate>(this); };
	auto Swizzle = [this]()
	{
		UInputModifierSwizzleAxis* M = NewObject<UInputModifierSwizzleAxis>(this);
		M->Order = EInputAxisSwizzle::YXZ;
		return M;
	};

	// WASD pan: D = +X, A = -X, W = +Y (swizzle), S = -Y (swizzle + negate)
	MoveAction = MakeAction(TEXT("IA_Move"), EInputActionValueType::Axis2D);
	Context->MapKey(MoveAction, EKeys::D);
	Context->MapKey(MoveAction, EKeys::A).Modifiers.Add(Negate());
	Context->MapKey(MoveAction, EKeys::W).Modifiers.Add(Swizzle());
	{
		FEnhancedActionKeyMapping& S = Context->MapKey(MoveAction, EKeys::S);
		S.Modifiers.Add(Swizzle());
		S.Modifiers.Add(Negate());
	}

	ZoomAction = MakeAction(TEXT("IA_Zoom"), EInputActionValueType::Axis1D);
	Context->MapKey(ZoomAction, EKeys::MouseWheelAxis);

	OrbitAction = MakeAction(TEXT("IA_Orbit"), EInputActionValueType::Boolean);
	Context->MapKey(OrbitAction, EKeys::RightMouseButton);

	PrimaryAction = MakeAction(TEXT("IA_Primary"), EInputActionValueType::Boolean);
	Context->MapKey(PrimaryAction, EKeys::LeftMouseButton);

	RotateAction = MakeAction(TEXT("IA_Rotate"), EInputActionValueType::Axis1D);
	Context->MapKey(RotateAction, EKeys::E);
	Context->MapKey(RotateAction, EKeys::Q).Modifiers.Add(Negate());

	DeleteAction = MakeAction(TEXT("IA_Delete"), EInputActionValueType::Boolean);
	Context->MapKey(DeleteAction, EKeys::Delete);
	Context->MapKey(DeleteAction, EKeys::BackSpace);

	ActionAction = MakeAction(TEXT("IA_Action"), EInputActionValueType::Boolean);
	Context->MapKey(ActionAction, EKeys::SpaceBar);

	const FKey CueKeys[UTakeDirectorSubsystem::NumCueSlots] = { EKeys::One, EKeys::Two, EKeys::Three };
	for (int32 i = 0; i < UTakeDirectorSubsystem::NumCueSlots; ++i)
	{
		UInputAction* A = MakeAction(*FString::Printf(TEXT("IA_Cue%d"), i + 1), EInputActionValueType::Boolean);
		Context->MapKey(A, CueKeys[i]);
		CueActions.Add(A);
	}
}

void ADirectorPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	BuildInput();

	if (const APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (ULocalPlayer* LP = PC->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Sub = LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
			{
				Sub->AddMappingContext(Context, 0);
			}
		}
	}

	UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
	if (!EIC)
	{
		UE_LOG(LogTake37, Error, TEXT("DirectorPawn: Enhanced Input component missing. Check DefaultInput.ini."));
		return;
	}
	EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ADirectorPawn::OnMove);
	EIC->BindAction(MoveAction, ETriggerEvent::Completed, this, &ADirectorPawn::OnMoveCompleted);
	EIC->BindAction(ZoomAction, ETriggerEvent::Triggered, this, &ADirectorPawn::OnZoom);
	EIC->BindAction(OrbitAction, ETriggerEvent::Started, this, &ADirectorPawn::OnOrbitStarted);
	EIC->BindAction(OrbitAction, ETriggerEvent::Completed, this, &ADirectorPawn::OnOrbitCompleted);
	EIC->BindAction(PrimaryAction, ETriggerEvent::Started, this, &ADirectorPawn::OnPrimaryStarted);
	EIC->BindAction(PrimaryAction, ETriggerEvent::Completed, this, &ADirectorPawn::OnPrimaryCompleted);
	EIC->BindAction(RotateAction, ETriggerEvent::Triggered, this, &ADirectorPawn::OnRotate);
	EIC->BindAction(DeleteAction, ETriggerEvent::Started, this, &ADirectorPawn::OnDelete);
	EIC->BindAction(ActionAction, ETriggerEvent::Started, this, &ADirectorPawn::OnActionKey);
	for (int32 i = 0; i < CueActions.Num(); ++i)
	{
		EIC->BindAction(CueActions[i], ETriggerEvent::Started, this, &ADirectorPawn::OnCue, i);
	}
}

void ADirectorPawn::OnMove(const FInputActionValue& Value)
{
	MoveInput = Value.Get<FVector2D>();
}

void ADirectorPawn::OnMoveCompleted()
{
	MoveInput = FVector2D::ZeroVector;
}

void ADirectorPawn::OnZoom(const FInputActionValue& Value)
{
	ArmLength = FMath::Clamp(ArmLength - Value.Get<float>() * 160.f, 350.f, 3600.f);
}

void ADirectorPawn::OnRotate(const FInputActionValue& Value)
{
	if (Placement)
	{
		Placement->RotateSelected(Value.Get<float>() * 120.f * GetWorld()->GetDeltaSeconds());
	}
}

void ADirectorPawn::OnDelete()
{
	if (Placement)
	{
		Placement->DeleteSelected();
	}
}

void ADirectorPawn::OnActionKey()
{
	UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>();
	if (!Dir)
	{
		return;
	}
	switch (Dir->GetPhase())
	{
	case ETake37Phase::Setup: Dir->RequestAction(); break;
	case ETake37Phase::Take: Dir->RequestCut(); break;
	case ETake37Phase::Results: Dir->RequestRetry(); break;
	default: break;
	}
}

void ADirectorPawn::OnCue(int32 Slot)
{
	UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>();
	if (!Dir)
	{
		return;
	}
	if (Dir->GetPhase() == ETake37Phase::Take)
	{
		Dir->FireCue(Slot);
	}
	else if (Dir->GetPhase() == ETake37Phase::Setup && Placement && Placement->GetSelectedDevice())
	{
		Dir->AssignCue(Slot, Placement->GetSelectedDevice());
	}
}

void ADirectorPawn::OnPrimaryStarted()
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>();
	if (!PC || !Dir)
	{
		return;
	}
	// HUD buttons first.
	float X = 0.f, Y = 0.f;
	if (const ATake37HUD* HUD = Cast<ATake37HUD>(PC->GetHUD()))
	{
		if (PC->GetMousePosition(X, Y))
		{
			const FName Button = HUD->HitTestButton(FVector2D(X, Y));
			if (Button != NAME_None)
			{
				HandleButton(Button);
				return;
			}
		}
	}
	if (Dir->GetPhase() == ETake37Phase::Setup && Placement)
	{
		Placement->PrimaryPressed(PC);
	}
}

void ADirectorPawn::OnPrimaryCompleted()
{
	if (Placement)
	{
		Placement->PrimaryReleased();
	}
}

void ADirectorPawn::HandleButton(FName Button)
{
	UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>();
	if (!Dir)
	{
		return;
	}
	const FString Name = Button.ToString();
	if (Name == TEXT("Action"))
	{
		Dir->RequestAction();
	}
	else if (Name == TEXT("Cut"))
	{
		Dir->RequestCut();
	}
	else if (Name == TEXT("Retry"))
	{
		Dir->RequestRetry();
	}
	else if (Name.StartsWith(TEXT("Cart_")) && Placement && Dir->GetPhase() == ETake37Phase::Setup)
	{
		Placement->ToggleArmed(static_cast<ECartItem>(FCString::Atoi(*Name.RightChop(5))));
	}
	else if (Name.StartsWith(TEXT("Cue_")))
	{
		OnCue(FCString::Atoi(*Name.RightChop(4)));
	}
}

void ADirectorPawn::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC)
	{
		return;
	}

	// RMB drag orbits. Mouse deltas come from cursor movement so the cursor can stay visible.
	float MX = 0.f, MY = 0.f;
	if (bOrbit && PC->GetMousePosition(MX, MY))
	{
		const FVector2D Cur(MX, MY);
		if (bHasLastMouse)
		{
			Yaw += (Cur.X - LastMouse.X) * 0.25f;
			Pitch = FMath::Clamp(Pitch - (Cur.Y - LastMouse.Y) * 0.25f, -80.f, -10.f);
		}
		LastMouse = Cur;
		bHasLastMouse = true;
	}
	else
	{
		bHasLastMouse = false;
	}

	const FRotator YawRot(0.f, Yaw, 0.f);
	const FVector Fwd = YawRot.Vector();
	const FVector Right = FRotationMatrix(YawRot).GetScaledAxis(EAxis::Y);
	const float Speed = 900.f * (ArmLength / 1500.f);
	Pivot += (Fwd * MoveInput.Y + Right * MoveInput.X) * Speed * DeltaTime;
	Pivot.X = FMath::Clamp(Pivot.X, -1600.0, 1600.0);
	Pivot.Y = FMath::Clamp(Pivot.Y, -1100.0, 1100.0);
	SetActorLocation(Pivot);

	Arm->TargetArmLength = ArmLength;
	Arm->SetWorldRotation(FRotator(Pitch, Yaw, 0.f));

	if (Placement)
	{
		Placement->TickPlacement(PC, DeltaTime);
	}
}
