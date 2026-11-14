#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Chain/PropVisuals.h"
#include "CueDeviceActor.generated.h"

class UBoxComponent;
class UChainPropComponent;
class ATake37PropActor;

UENUM(BlueprintType)
enum class ECueType : uint8
{
	Sandbag,
	Chandelier,
	Pyro,
	Wind,
};

/** Cue-able set device: sandbag release, chandelier winch, pyro puff, wind machine (GDD section 5.3). */
UCLASS()
class TAKE37_API ACueDeviceActor : public AActor
{
	GENERATED_BODY()

public:
	ACueDeviceActor();

	UPROPERTY() TObjectPtr<UBoxComponent> Body;
	UPROPERTY() TObjectPtr<UChainPropComponent> ChainProp;
	/** Held object released by Sandbag / Chandelier cues. */
	UPROPERTY() TObjectPtr<ATake37PropActor> Payload;

	UPROPERTY(EditAnywhere) ECueType CueType = ECueType::Sandbag;
	UPROPERTY(EditAnywhere) FString DisplayName;
	UPROPERTY(EditAnywhere) float Radius = 450.f;
	UPROPERTY(EditAnywhere) float Strength = 40000.f;

	bool bFired = false;

	/** Size is in metres (1.0 = 100 cm); Kind selects the model in PropVisuals. */
	void Setup(ECueType InType, const FString& InName, const FVector& Size, const FLinearColor& Color, const FString& Kind);
	void Fire();
	void ResetCue();
	void SetHighlight(bool bOn);

private:
	TArray<FVisualPart> Visuals;
};
