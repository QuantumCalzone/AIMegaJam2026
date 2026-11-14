#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "ScoringConfig.generated.h"

/** All score and chain constants (GDD section 4.3). Tune in Data Assets or here. */
UCLASS(BlueprintType)
class TAKE37_API UScoringConfig : public UDataAsset
{
	GENERATED_BODY()

public:
	/** LinkScore = BaseValue * (1 + DepthBonus * Depth) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score") float DepthBonus = 0.5f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score") float ImprovMultiplier = 2.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score") float VarietyBonus = 150.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score") float DirectorEyePercent = 0.2f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combo") float ComboWindow = 1.5f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combo") float ComboStep = 0.25f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combo") float ComboMax = 3.f;

	/** A prop stays a valid chain source for this long after it was credited (seconds). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") float ChainContinueWindow = 3.f;
	/** Speed (cm/s) at which an origin-capable prop that is moving on its own starts a chain. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") float OriginSpeed = 120.f;

	/** Impulse above which a link triggers hit-stop (GDD section 8.2). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Feel") float BigHitImpulse = 12000.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Feel") float HitStopDilation = 0.25f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Feel") float HitStopDuration = 0.3f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Feel") float HitStopCooldown = 2.f;
};
