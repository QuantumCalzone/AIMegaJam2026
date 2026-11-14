#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Core/Take37Types.h"
#include "ChallengeDefinition.generated.h"

/**
 * One scene/challenge (GDD section 3.2). M1 default: hit the $2M Hero Camera at the end of a 3+ link chain
 * (Scene 3 "The Stunt", scaled down because the actors are not in yet).
 */
UCLASS(BlueprintType)
class TAKE37_API UChallengeDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UChallengeDefinition();

	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString SceneName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString ObjectiveText;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Genre = TEXT("Western");

	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 SabotageBudget = 1000;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float TakeTimeLimit = 45.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) TArray<ECartItem> AvailableItems;

	/** Star 1: Hero Camera hit by a chain of at least this many links. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 MinChainForObjective = 3;
	/** Star 2: objective plus this much Box Office. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Star2Score = 3000;
	/** Star 3: objective, Star 2 and a chain of at least this many links. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Star3Chain = 5;
};
