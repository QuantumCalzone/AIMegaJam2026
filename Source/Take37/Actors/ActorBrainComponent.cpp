#include "Actors/ActorBrainComponent.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "HAL/IConsoleManager.h"
#include "Take37.h"

static TAutoConsoleVariable<int32> CVarShowBrain(TEXT("t37.ShowBrain"), 0, TEXT("1 = log each actor's reaction choices."), ECVF_Default);

namespace
{
	constexpr float StumbleImpulse = 1200.f;
	constexpr float RagdollImpulse = 4500.f;
}

UActorBrainComponent::UActorBrainComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UActorBrainComponent::BeginPlay()
{
	Super::BeginPlay();
	Chain = GetWorld()->GetSubsystem<UChainReactionSubsystem>();
	if (Chain.IsValid())
	{
		Chain->OnLink.AddUObject(this, &UActorBrainComponent::HandleLink);
	}
}

void UActorBrainComponent::EndPlay(const EEndPlayReason::Type Reason)
{
	if (Chain.IsValid())
	{
		Chain->OnLink.RemoveAll(this);
	}
	Super::EndPlay(Reason);
}

void UActorBrainComponent::Reset()
{
	Composure = 1.f;
	LastReactTime = -100.0;
	for (double& C : Cooldown)
	{
		C = 0.0;
	}
}

AStageActorCharacter* UActorBrainComponent::FindGrudgeTarget(AStageActorCharacter* Me) const
{
	for (TActorIterator<AStageActorCharacter> It(GetWorld()); It; ++It)
	{
		if (*It != Me && It->DisplayName == Traits.GrudgeTarget && !It->IsOut())
		{
			return *It;
		}
	}
	return nullptr;
}

/** Put this actor into the chain that triggered its reaction so anything it knocks over scores as IMPROV. */
void UActorBrainComponent::JoinChain(const FChainLink& Link, AStageActorCharacter* Me)
{
	if (UChainPropComponent* P = Me->GetChainProp())
	{
		if (P->ChainId == INDEX_NONE || !P->IsChainActive(GetWorld()->GetTimeSeconds(), 3.f))
		{
			P->ChainId = Link.ChainId;
			P->ChainDepth = Link.Depth + 1;
		}
		P->LastCreditTime = GetWorld()->GetTimeSeconds();
		P->bImprov = true;
	}
}

void UActorBrainComponent::HandleLink(const FChainLink& Link)
{
	AStageActorCharacter* Me = Cast<AStageActorCharacter>(GetOwner());
	if (!Me || !Chain.IsValid() || !Chain->IsTakeActive() || Me->IsOut() || Me->IsDown())
	{
		return;
	}
	if (Link.ToName == FName(*Me->DisplayName))
	{
		HandleSelfHit(Link, Me);
	}
	else
	{
		Perceive(Link, Me);
	}
}

void UActorBrainComponent::HandleSelfHit(const FChainLink& Link, AStageActorCharacter* Me)
{
	Composure = FMath::Max(0.f, Composure - 0.25f);
	JoinChain(Link, Me);
	LastReactTime = GetWorld()->GetTimeSeconds();

	if (Link.Impulse >= RagdollImpulse)
	{
		FVector Dir = (Link.ToLocation - Link.FromLocation).GetSafeNormal2D();
		Me->Bark(TEXT("Hurt_Heavy"));
		Me->DoRagdoll(Dir * 450.f + FVector(0, 0, 250.f));
	}
	else
	{
		Me->Bark(TEXT("Hurt_Light"));
		Me->DoRecoil(Link.FromLocation, 0.5f);
	}
}

void UActorBrainComponent::Perceive(const FChainLink& Link, AStageActorCharacter* Me)
{
	const double Now = GetWorld()->GetTimeSeconds();
	const float Dist = FVector::Dist2D(Me->GetActorLocation(), Link.ToLocation);
	const float Radius = 350.f + FMath::Min(Link.Impulse * 0.04f, 1100.f);
	if (Dist > Radius || (Now - LastReactTime) < 2.f)
	{
		return;
	}

	// Utility scoring: personality weights + context + a little randomness, minus recent use (GDD section 6.4).
	float U[static_cast<int32>(EReaction::Count)];
	const bool bBig = Link.Impulse > 6000.f;
	const bool bPrecious = Link.ToCategory == EChainCategory::Camera;
	AStageActorCharacter* Grudge = FindGrudgeTarget(Me);
	const bool bGrudgeNear = Grudge && FVector::Dist2D(Grudge->GetActorLocation(), Me->GetActorLocation()) < 800.f;

	U[static_cast<int32>(EReaction::DoubleTake)] = 0.3f;
	U[static_cast<int32>(EReaction::Shriek)] = Traits.Drama * 0.5f + Traits.Panic * 0.5f;
	U[static_cast<int32>(EReaction::PanicRun)] = Traits.Panic * 1.0f + (bBig ? 0.3f : 0.f);
	U[static_cast<int32>(EReaction::Faint)] = Traits.Drama * 0.8f + (bBig ? 0.35f : 0.f) - Composure * 0.15f;
	U[static_cast<int32>(EReaction::HeroicDive)] = Traits.Bravado * 1.0f + (bPrecious ? 0.5f : 0.f);
	U[static_cast<int32>(EReaction::Blame)] = bGrudgeNear ? (Traits.Drama * 0.3f + Traits.Grudge * 0.8f) : -1.f;
	U[static_cast<int32>(EReaction::Pose)] = Traits.Vanity * 0.3f;
	U[static_cast<int32>(EReaction::StormOff)] = (Composure < 0.35f && Traits.Drama > 0.7f) ? 2.f : -1.f;

	int32 Best = 0;
	for (int32 i = 0; i < static_cast<int32>(EReaction::Count); ++i)
	{
		U[i] += FMath::FRandRange(0.f, 0.15f);
		if (Now < Cooldown[i])
		{
			U[i] -= 1.f;
		}
		if (U[i] > U[Best])
		{
			Best = i;
		}
	}
	if (U[Best] < 0.2f)
	{
		return;
	}
	if (CVarShowBrain.GetValueOnGameThread() > 0)
	{
		UE_LOG(LogTake37, Log, TEXT("%s reacts: %d (utility %.2f, composure %.2f)"), *Me->DisplayName, Best, U[Best], Composure);
	}
	Composure = FMath::Max(0.f, Composure - 0.15f);
	LastReactTime = Now;
	Cooldown[Best] = Now + 6.0;
	JoinChain(Link, Me);
	Execute(static_cast<EReaction>(Best), Link, Me);
}

void UActorBrainComponent::Execute(EReaction R, const FChainLink& Link, AStageActorCharacter* Me)
{
	const FVector Event = Link.ToLocation;
	switch (R)
	{
	case EReaction::DoubleTake:
		Me->DoFace(Event);
		Me->DoHop();
		Me->Bark(TEXT("Notice"));
		break;
	case EReaction::Shriek:
		Me->DoFace(Event);
		Me->Bark(TEXT("Panic"));
		Me->DoRecoil(Event, 0.8f);
		break;
	case EReaction::PanicRun:
		Me->Bark(TEXT("Panic"));
		Me->DoPanicRun(2.6f);
		break;
	case EReaction::Faint:
	{
		Me->Bark(TEXT("Faint"));
		// Faint toward the nearest prop so the collapse has consequences.
		FVector Dir = (Me->GetActorLocation() - Event).GetSafeNormal2D();
		float BestD = 400.f;
		for (const TWeakObjectPtr<UChainPropComponent>& P : Chain->GetProps())
		{
			if (P.IsValid() && P->GetOwner() && P->Category != EChainCategory::Actor && P->GetBoundPrimitive() && P->GetBoundPrimitive()->IsSimulatingPhysics())
			{
				const float D = FVector::Dist2D(P->GetOwner()->GetActorLocation(), Me->GetActorLocation());
				if (D < BestD)
				{
					BestD = D;
					Dir = (P->GetOwner()->GetActorLocation() - Me->GetActorLocation()).GetSafeNormal2D();
				}
			}
		}
		Me->DoRagdoll(Dir * 320.f + FVector(0, 0, 120.f));
		break;
	}
	case EReaction::HeroicDive:
		Me->Bark(TEXT("Heroic"));
		Me->DoDive(Event);
		break;
	case EReaction::Blame:
		if (AStageActorCharacter* Target = FindGrudgeTarget(Me))
		{
			Me->Bark(TEXT("Blame"));
			Me->DoShove(Target);
		}
		break;
	case EReaction::Pose:
		Me->Bark(TEXT("Pose"));
		Me->DoPose(1.8f);
		break;
	case EReaction::StormOff:
		Me->Bark(TEXT("StormOff"));
		Me->DoStormOff();
		break;
	default:
		break;
	}
}
