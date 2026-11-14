#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Chain/ChainTypes.h"
#include "ChainPropComponent.generated.h"

/** Marks a physics object as score-able and carries its chain state (GDD section 4.1). */
UCLASS(ClassGroup = Take37, meta = (BlueprintSpawnableComponent))
class TAKE37_API UChainPropComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UChainPropComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") EChainCategory Category = EChainCategory::Furniture;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") FString DisplayName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") float BaseValue = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") float DollarValue = 0.f;
	/** Hits below this impulse (kg*cm/s) are ignored as jitter. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") float MinImpulseToCount = 1500.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") bool bExpensive = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") bool bFragile = false;
	/** May start a chain on its own when it begins moving (sandbag, bowling ball...). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") bool bCanOriginChain = false;
	/** Bind to the owner's root primitive hit events. Cue devices turn this off. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chain") bool bListenForHits = true;

	// Runtime state
	int32 ChainId = INDEX_NONE;
	int32 ChainDepth = 0;
	TWeakObjectPtr<UChainPropComponent> LastInstigator;
	double LastCreditTime = -1000.0;
	bool bImprov = false;

	bool IsChainActive(double Now, float Window) const { return ChainId != INDEX_NONE && (Now - LastCreditTime) <= Window; }
	void ResetRuntime();
	UPrimitiveComponent* GetBoundPrimitive() const { return BoundPrim.Get(); }
	FString GetLabel() const;

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	UFUNCTION()
	void OnOwnerHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit);

private:
	TWeakObjectPtr<UPrimitiveComponent> BoundPrim;
};
