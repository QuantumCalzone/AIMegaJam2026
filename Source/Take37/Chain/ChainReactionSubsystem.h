#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "Chain/ChainTypes.h"
#include "ChainReactionSubsystem.generated.h"

class UChainPropComponent;
class UScoringConfig;

/**
 * Causal graph, link events, combo, score and event log (GDD sections 4.2 - 4.4).
 * Props report hits; the subsystem decides which direction credit flows.
 */
UCLASS()
class TAKE37_API UChainReactionSubsystem : public UTickableWorldSubsystem
{
	GENERATED_BODY()

public:
	virtual bool DoesSupportWorldType(const EWorldType::Type WorldType) const override;
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Tick(float DeltaTime) override;
	virtual TStatId GetStatId() const override;

	void RegisterProp(UChainPropComponent* Prop);
	void UnregisterProp(UChainPropComponent* Prop);

	/** Begin scoring (physics is live). Does not clear previous results; call ResetTake first. */
	void BeginTake();
	void EndTake();
	/** Clears score, links, events and the chain state of every registered prop. */
	void ResetTake();
	bool IsTakeActive() const { return bTakeActive; }

	/** Start a new chain with Origin at depth 0. Returns the chain id. */
	int32 StartChain(UChainPropComponent* Origin, const FString& Reason);
	/** Collision report from a prop. Decides direction and credits a link when valid. */
	void ReportHit(UChainPropComponent* A, UChainPropComponent* B, float Impulse, const FVector& Location);
	/** Explicit link (cue devices and triggers). From must already be in a chain. */
	bool CreditLink(UChainPropComponent* From, UChainPropComponent* To, float Impulse, const FVector& Location, EChainLinkType Type, bool bImprov = false);

	void AddEvent(ETakeEventType Type, const FString& Text, float Score = 0.f, int32 ChainId = INDEX_NONE);

	// Stats
	float GetTotalScore() const { return TotalScore; }
	double GetDamages() const { return Damages; }
	int32 GetBestChainLinks() const { return BestChainLinks; }
	int32 GetLinkCount() const { return Links.Num(); }
	float GetComboMultiplier() const { return ComboMultiplier; }
	float GetLastLinkTime() const { return LastLinkTime; }
	float GetTakeStartTime() const { return TakeStartTime; }
	bool WasHeroCameraHit() const { return bHeroCameraHit; }
	int32 GetHeroCameraDepth() const { return HeroCameraDepth; }
	const TArray<FChainLink>& GetLinks() const { return Links; }
	const TArray<FTakeEvent>& GetEvents() const { return Events; }
	const TArray<TWeakObjectPtr<UChainPropComponent>>& GetProps() const { return Props; }
	UScoringConfig* GetConfig() const { return Config; }
	void SetConfig(UScoringConfig* InConfig);

	FOnChainLink OnLink;
	FOnScoreChanged OnScoreChanged;

private:
	struct FChainState
	{
		uint32 CategoryMask = 0;
		int32 Length = 0;
	};

	float Now() const;
	float UpdateCombo(float Time);

	UPROPERTY() TObjectPtr<UScoringConfig> Config;

	TArray<TWeakObjectPtr<UChainPropComponent>> Props;
	TMap<int32, FChainState> Chains;
	TArray<FChainLink> Links;
	TArray<FTakeEvent> Events;

	bool bTakeActive = false;
	int32 NextChainId = 1;
	float TakeStartTime = 0.f;
	float TotalScore = 0.f;
	double Damages = 0.0;
	int32 BestChainLinks = 0;
	float ComboMultiplier = 1.f;
	int32 ComboSteps = 0;
	float LastLinkTime = -1000.f;
	bool bHeroCameraHit = false;
	int32 HeroCameraDepth = -1;
};
