#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Actors/StageActorCharacter.h"
#include "Chain/ChainTypes.h"
#include "ActorBrainComponent.generated.h"

class UChainReactionSubsystem;

/**
 * Perception plus utility-scored reaction choice (GDD sections 6.3 and 6.4). Listens to chain links, decides whether
 * this actor notices, and picks one reaction by personality. Reactions run on the owning character; physics they
 * cause is credited into the triggering chain as IMPROV.
 */
UCLASS()
class TAKE37_API UActorBrainComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UActorBrainComponent();

	FActorTraits Traits;
	/** 1 = calm, 0 = meltdown. Drops with every accident seen or suffered. */
	float Composure = 1.f;

	void Reset();

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type Reason) override;

private:
	enum class EReaction : uint8 { DoubleTake, Shriek, PanicRun, Faint, HeroicDive, Blame, Pose, StormOff, Count };

	void HandleLink(const FChainLink& Link);
	void HandleSelfHit(const FChainLink& Link, AStageActorCharacter* Me);
	void Perceive(const FChainLink& Link, AStageActorCharacter* Me);
	void Execute(EReaction R, const FChainLink& Link, AStageActorCharacter* Me);
	AStageActorCharacter* FindGrudgeTarget(AStageActorCharacter* Me) const;
	void JoinChain(const FChainLink& Link, AStageActorCharacter* Me);

	double LastReactTime = -100.0;
	double Cooldown[static_cast<int32>(EReaction::Count)] = {};
	TWeakObjectPtr<UChainReactionSubsystem> Chain;
};
