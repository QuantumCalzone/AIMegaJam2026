#include "Core/Take37GameMode.h"
#include "Core/Take37Stage.h"
#include "Core/TakeDirectorSubsystem.h"
#include "Player/DirectorPawn.h"
#include "UI/Take37HUD.h"
#include "GameFramework/PlayerStart.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "TimerManager.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "UnrealClient.h"
#include "Misc/Paths.h"
#include "Take37.h"

ATake37GameMode::ATake37GameMode()
{
	DefaultPawnClass = ADirectorPawn::StaticClass();
	PlayerControllerClass = ATake37PlayerController::StaticClass();
	HUDClass = ATake37HUD::StaticClass();
}

AActor* ATake37GameMode::ChoosePlayerStart_Implementation(AController* Player)
{
	if (AActor* Start = Super::ChoosePlayerStart_Implementation(Player))
	{
		return Start;
	}
	if (!FallbackStart)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		FallbackStart = GetWorld()->SpawnActor<APlayerStart>(FVector(0, 0, 50), FRotator::ZeroRotator, Params);
	}
	return FallbackStart;
}

void ATake37GameMode::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogTake37, Log, TEXT("Take37GameMode: building stage"));
	GetWorld()->SpawnActor<ATake37Stage>(FVector::ZeroVector, FRotator::ZeroRotator);

	// Debug: -t37shot=<seconds> takes a screenshot of the Setup view; -t37shot2=<seconds> a second one (use with -ExecCmds t37.Action).
	float ShotDelay = 0.f;
	if (FParse::Value(FCommandLine::Get(), TEXT("-t37shot="), ShotDelay) && ShotDelay > 0.f)
	{
		FTimerHandle H;
		GetWorldTimerManager().SetTimer(H, [this]() { FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir() / TEXT("t37_shot_a.png"), false, false); }, ShotDelay, false);
	}
	float ActionDelay = 0.f;
	if (FParse::Value(FCommandLine::Get(), TEXT("-t37action="), ActionDelay) && ActionDelay > 0.f)
	{
		FTimerHandle HA;
		GetWorldTimerManager().SetTimer(HA, [this]()
		{
			if (UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>())
			{
				Dir->RequestAction();
				Dir->FireCue(0);
			}
		}, ActionDelay, false);
	}
	float ShotDelay2 = 0.f;
	if (FParse::Value(FCommandLine::Get(), TEXT("-t37shot2="), ShotDelay2) && ShotDelay2 > 0.f)
	{
		FTimerHandle H2;
		GetWorldTimerManager().SetTimer(H2, [this]() { FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir() / TEXT("t37_shot_b.png"), false, false); }, ShotDelay2, false);
	}
}

void ATake37PlayerController::BeginPlay()
{
	Super::BeginPlay();
	bShowMouseCursor = true;
	bEnableClickEvents = false;
	FInputModeGameAndUI Mode;
	Mode.SetHideCursorDuringCapture(false);
	Mode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
	SetInputMode(Mode);
}
