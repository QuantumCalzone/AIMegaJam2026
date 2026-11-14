#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/PlayerController.h"
#include "Take37GameMode.generated.h"

class APlayerStart;

/** Spawns the stage and wires up the director pawn, HUD and controller. Phase logic lives in UTakeDirectorSubsystem. */
UCLASS()
class TAKE37_API ATake37GameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ATake37GameMode();

	virtual void BeginPlay() override;
	virtual AActor* ChoosePlayerStart_Implementation(AController* Player) override;

private:
	UPROPERTY() TObjectPtr<APlayerStart> FallbackStart;
};

/** Shows the cursor and lets keyboard and mouse both reach the game. */
UCLASS()
class TAKE37_API ATake37PlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;
};
