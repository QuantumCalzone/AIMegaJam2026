#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "Core/Take37Types.h"
#include "Chain/ChainTypes.h"
#include "Core/Take37Stage.h"
#include "TakeDirectorSubsystem.generated.h"

class ACueDeviceActor;
class UChallengeDefinition;
class UChainReactionSubsystem;
class UBarkSubsystem;

DECLARE_MULTICAST_DELEGATE_TwoParams(FOnPhaseChanged, ETake37Phase /*Old*/, ETake37Phase /*New*/);

/** Score card for the Results screen (GDD section 2.3, text-only in M1). */
struct FTakeResults
{
	int64 Score = 0;
	int64 Damages = 0;
	int32 BestChain = 0;
	int32 LinkCount = 0;
	bool bHeroHit = false;
	int32 HeroDepth = -1;
	int32 Stars = 0;
	FString TopLink;
	FString CriticName;
	FString Publication;
	FString Headline;
	FString Review;
	FString PullQuote;
};

/** Owns the phase machine and the take timer (GDD sections 2 and 12.2). */
UCLASS()
class TAKE37_API UTakeDirectorSubsystem : public UTickableWorldSubsystem
{
	GENERATED_BODY()

public:
	static constexpr int32 NumCueSlots = 3;

	virtual bool DoesSupportWorldType(const EWorldType::Type WorldType) const override;
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
	virtual void Tick(float DeltaTime) override;
	virtual TStatId GetStatId() const override;

	void RegisterStage(ATake37Stage* InStage) { Stage = InStage; }

	/** Enter Setup. Used at level start and for Retry. */
	void StartSetup();
	void RequestAction();
	/** Skip to CUT; allowed after 5 s of the take. */
	void RequestCut();
	void RequestRetry();
	bool FireCue(int32 Slot);
	void AssignCue(int32 Slot, ACueDeviceActor* Device);
	ACueDeviceActor* GetCueDevice(int32 Slot) const;

	ETake37Phase GetPhase() const { return Phase; }
	float GetTakeTime() const { return TakeTime; }
	float GetTakeTimeLimit() const;
	UChallengeDefinition* GetChallenge() const { return Challenge; }
	const FTakeResults& GetResults() const { return Results; }
	int32 GetTakeNumber() const { return TakeNumber; }

	FOnPhaseChanged OnPhaseChanged;

private:
	void SetPhase(ETake37Phase NewPhase);
	void EndTake(const TCHAR* Reason);
	void ShowResults();
	void BuildResults();
	void HandleLink(const FChainLink& Link);
	void Bark(FName Actor, FName Tag, int32 MinIntensity = 0);

	UPROPERTY() TObjectPtr<UChallengeDefinition> Challenge;
	TWeakObjectPtr<ATake37Stage> Stage;
	TWeakObjectPtr<UChainReactionSubsystem> Chain;
	TWeakObjectPtr<UBarkSubsystem> Barks;
	TArray<TWeakObjectPtr<ACueDeviceActor>> CueSlots;

	ETake37Phase Phase = ETake37Phase::Setup;
	float PhaseTime = 0.f;
	float TakeTime = 0.f;
	int32 TakeNumber = 1;
	FTakeResults Results;

	double LastHitStopReal = -100.0;
	double HitStopEndsReal = 0.0;
	bool bHitStopActive = false;
};
