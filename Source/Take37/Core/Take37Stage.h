#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Core/Take37Types.h"
#include "Chain/CueDeviceActor.h"
#include "Chain/Take37PropActor.h"
#include "Actors/StageActorCharacter.h"
#include "Take37Stage.generated.h"

/**
 * Builds the greybox soundstage at runtime and resets it between takes (GDD section 3.1).
 * Greybox only: real set dressing replaces these shapes later, keeping the same ChainProp setup.
 */
UCLASS()
class TAKE37_API ATake37Stage : public AActor
{
	GENERATED_BODY()

public:
	ATake37Stage();

	/** Track a prop for reset/physics (used by Placement for player-placed items). */
	void RegisterProp(ATake37PropActor* Prop);
	void UnregisterProp(ATake37PropActor* Prop);

	ATake37PropActor* SpawnProp(const FPropSpec& Spec, const FVector& BottomLocation, const FRotator& Rotation = FRotator::ZeroRotator, bool bLocationIsCenter = false);

	const TArray<TObjectPtr<ACueDeviceActor>>& GetDevices() const { return Devices; }

protected:
	virtual void BeginPlay() override;

private:
	void BuildLighting();
	void BuildStage();
	void BuildCast();
	ACueDeviceActor* SpawnDevice(ECueType Type, const FString& Name, const FVector& BottomLocation, const FVector& Size, const FLinearColor& Color, const FString& Kind, float Yaw = 0.f);
	void AddSign(const FString& Text, const FVector& Location, float WorldSize, const FColor& Color);
	void HandlePhaseChanged(ETake37Phase Old, ETake37Phase New);
	void ResetAll();

	UPROPERTY() TArray<TObjectPtr<ATake37PropActor>> Props;
	UPROPERTY() TArray<TObjectPtr<ACueDeviceActor>> Devices;
	UPROPERTY() TArray<TObjectPtr<AStageActorCharacter>> Actors;
};
