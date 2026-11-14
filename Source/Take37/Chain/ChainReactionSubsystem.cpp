#include "Chain/ChainReactionSubsystem.h"
#include "Chain/ChainPropComponent.h"
#include "Core/ScoringConfig.h"
#include "Components/PrimitiveComponent.h"
#include "DrawDebugHelpers.h"
#include "Engine/World.h"
#include "HAL/IConsoleManager.h"
#include "Take37.h"

static TAutoConsoleVariable<int32> CVarShowChains(
	TEXT("t37.ShowChains"), 0,
	TEXT("1 = draw chain links with depth labels in the world."),
	ECVF_Default);

bool UChainReactionSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
	return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}

void UChainReactionSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	Config = NewObject<UScoringConfig>(this, TEXT("DefaultScoringConfig"));
}

TStatId UChainReactionSubsystem::GetStatId() const
{
	RETURN_QUICK_DECLARE_CYCLE_STAT(UChainReactionSubsystem, STATGROUP_Tickables);
}

void UChainReactionSubsystem::SetConfig(UScoringConfig* InConfig)
{
	if (InConfig)
	{
		Config = InConfig;
	}
}

float UChainReactionSubsystem::Now() const
{
	return GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
}

void UChainReactionSubsystem::RegisterProp(UChainPropComponent* Prop)
{
	if (Prop)
	{
		Props.AddUnique(Prop);
	}
}

void UChainReactionSubsystem::UnregisterProp(UChainPropComponent* Prop)
{
	Props.Remove(Prop);
}

void UChainReactionSubsystem::ResetTake()
{
	bTakeActive = false;
	Chains.Reset();
	Links.Reset();
	Events.Reset();
	NextChainId = 1;
	TotalScore = 0.f;
	Damages = 0.0;
	BestChainLinks = 0;
	ComboMultiplier = 1.f;
	ComboSteps = 0;
	LastLinkTime = -1000.f;
	bHeroCameraHit = false;
	HeroCameraDepth = -1;
	for (const TWeakObjectPtr<UChainPropComponent>& P : Props)
	{
		if (P.IsValid())
		{
			P->ResetRuntime();
		}
	}
	OnScoreChanged.Broadcast();
}

void UChainReactionSubsystem::BeginTake()
{
	TakeStartTime = Now();
	bTakeActive = true;
	AddEvent(ETakeEventType::Phase, TEXT("ACTION!"));
}

void UChainReactionSubsystem::EndTake()
{
	bTakeActive = false;
}

void UChainReactionSubsystem::AddEvent(ETakeEventType Type, const FString& Text, float Score, int32 ChainId)
{
	FTakeEvent E;
	E.Time = Now() - TakeStartTime;
	E.Type = Type;
	E.Text = Text;
	E.Score = Score;
	E.ChainId = ChainId;
	Events.Add(E);
}

float UChainReactionSubsystem::UpdateCombo(float Time)
{
	if (Config && (Time - LastLinkTime) <= Config->ComboWindow)
	{
		++ComboSteps;
	}
	else
	{
		ComboSteps = 0;
	}
	const float Step = Config ? Config->ComboStep : 0.25f;
	const float Max = Config ? Config->ComboMax : 3.f;
	ComboMultiplier = FMath::Min(Max, 1.f + Step * ComboSteps);
	LastLinkTime = Time;
	return ComboMultiplier;
}

int32 UChainReactionSubsystem::StartChain(UChainPropComponent* Origin, const FString& Reason)
{
	if (!Origin || !bTakeActive || Origin->ChainId != INDEX_NONE)
	{
		return Origin ? Origin->ChainId : INDEX_NONE;
	}

	const float T = Now();
	const int32 Id = NextChainId++;
	Origin->ChainId = Id;
	Origin->ChainDepth = 0;
	Origin->LastCreditTime = T;
	Origin->bImprov = false;

	FChainState& State = Chains.Add(Id);
	State.CategoryMask = 1u << static_cast<uint32>(Origin->Category);

	const float Mult = UpdateCombo(T);
	const float Score = Origin->BaseValue * Mult;
	TotalScore += Score;
	Damages += Origin->DollarValue;
	BestChainLinks = FMath::Max(BestChainLinks, 1);

	FChainLink Link;
	Link.ChainId = Id;
	Link.FromName = FName(*Reason);
	Link.ToName = FName(*Origin->GetLabel());
	Link.Depth = 0;
	Link.Time = T - TakeStartTime;
	Link.FromLocation = Link.ToLocation = Origin->GetOwner() ? Origin->GetOwner()->GetActorLocation() : FVector::ZeroVector;
	Link.LinkType = EChainLinkType::Origin;
	Link.ToCategory = Origin->Category;
	Link.Score = Score;
	Link.ComboMultiplier = Mult;
	Links.Add(Link);

	AddEvent(ETakeEventType::Link, FString::Printf(TEXT("%s: %s starts chain %d"), *Reason, *Origin->GetLabel(), Id), Score, Id);
	UE_LOG(LogTake37, Log, TEXT("Chain %d started by %s (%s) +%.0f"), Id, *Origin->GetLabel(), *Reason, Score);
	OnLink.Broadcast(Link);
	OnScoreChanged.Broadcast();
	return Id;
}

void UChainReactionSubsystem::ReportHit(UChainPropComponent* A, UChainPropComponent* B, float Impulse, const FVector& Location)
{
	if (!bTakeActive || !A || !B || !Config)
	{
		return;
	}
	const double T = Now();
	const bool bAActive = A->IsChainActive(T, Config->ChainContinueWindow);
	const bool bBActive = B->IsChainActive(T, Config->ChainContinueWindow);

	UChainPropComponent* From = nullptr;
	if (bAActive && bBActive)
	{
		if (A->ChainId == B->ChainId)
		{
			return;
		}
		From = (A->ChainDepth <= B->ChainDepth) ? A : B;
	}
	else if (bAActive)
	{
		From = A;
	}
	else if (bBActive)
	{
		From = B;
	}
	else
	{
		return;
	}

	UChainPropComponent* To = (From == A) ? B : A;
	if (Impulse < To->MinImpulseToCount)
	{
		return;
	}
	CreditLink(From, To, Impulse, Location, EChainLinkType::Collision, From->bImprov);
}

bool UChainReactionSubsystem::CreditLink(UChainPropComponent* From, UChainPropComponent* To, float Impulse, const FVector& Location, EChainLinkType Type, bool bImprov)
{
	if (!bTakeActive || !From || !To || !Config || From->ChainId == INDEX_NONE)
	{
		return false;
	}
	// A prop scores once per chain; this stops loops from farming points.
	if (To->ChainId == From->ChainId)
	{
		return false;
	}

	const float T = Now();
	const int32 ChainId = From->ChainId;
	const int32 Depth = From->ChainDepth + 1;

	To->ChainId = ChainId;
	To->ChainDepth = Depth;
	To->LastInstigator = From;
	To->LastCreditTime = T;
	To->bImprov = bImprov;

	const float Mult = UpdateCombo(T);
	const float LinkScore = To->BaseValue * (1.f + Config->DepthBonus * Depth) * (bImprov ? Config->ImprovMultiplier : 1.f);
	float Added = LinkScore * Mult;

	FChainState& State = Chains.FindOrAdd(ChainId);
	const uint32 Bit = 1u << static_cast<uint32>(To->Category);
	if ((State.CategoryMask & Bit) == 0)
	{
		State.CategoryMask |= Bit;
		Added += Config->VarietyBonus;
	}
	State.Length += 1;
	BestChainLinks = FMath::Max(BestChainLinks, State.Length + 1);

	TotalScore += Added;
	Damages += To->DollarValue;

	if (To->bExpensive && To->Category == EChainCategory::Camera && !bHeroCameraHit)
	{
		bHeroCameraHit = true;
		HeroCameraDepth = Depth;
	}

	FChainLink Link;
	Link.ChainId = ChainId;
	Link.FromName = FName(*From->GetLabel());
	Link.ToName = FName(*To->GetLabel());
	Link.Depth = Depth;
	Link.Impulse = Impulse;
	Link.Time = T - TakeStartTime;
	Link.FromLocation = From->GetOwner() ? From->GetOwner()->GetActorLocation() : Location;
	Link.ToLocation = To->GetOwner() ? To->GetOwner()->GetActorLocation() : Location;
	Link.LinkType = Type;
	Link.ToCategory = To->Category;
	Link.bImprov = bImprov;
	Link.Score = Added;
	Link.ComboMultiplier = Mult;
	Links.Add(Link);

	AddEvent(ETakeEventType::Link, FString::Printf(TEXT("%s -> %s (depth %d, impulse %.0f)"), *From->GetLabel(), *To->GetLabel(), Depth, Impulse), Added, ChainId);
	UE_LOG(LogTake37, Log, TEXT("Chain %d link %s -> %s depth %d impulse %.0f +%.0f (combo x%.2f)"),
		ChainId, *From->GetLabel(), *To->GetLabel(), Depth, Impulse, Added, Mult);

	OnLink.Broadcast(Link);
	OnScoreChanged.Broadcast();
	return true;
}

void UChainReactionSubsystem::Tick(float DeltaTime)
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	if (bTakeActive && Config)
	{
		const float T = Now();
		// Props that start moving on their own (gravity release) become chain origins.
		if (T - TakeStartTime > 0.75f)
		{
			const float SpeedSq = FMath::Square(Config->OriginSpeed);
			for (const TWeakObjectPtr<UChainPropComponent>& P : Props)
			{
				UChainPropComponent* Prop = P.Get();
				if (!Prop || !Prop->bCanOriginChain || Prop->ChainId != INDEX_NONE)
				{
					continue;
				}
				UPrimitiveComponent* Prim = Prop->GetBoundPrimitive();
				if (Prim && Prim->IsSimulatingPhysics() && Prim->GetPhysicsLinearVelocity().SizeSquared() > SpeedSq)
				{
					StartChain(Prop, TEXT("Gravity release"));
				}
			}
		}
	}

	if (CVarShowChains.GetValueOnGameThread() > 0)
	{
		const float T = Now() - TakeStartTime;
		for (const FChainLink& L : Links)
		{
			if (T - L.Time > 6.f)
			{
				continue;
			}
			DrawDebugLine(World, L.FromLocation, L.ToLocation, FColor::Yellow, false, 0.f, 0, 4.f);
			DrawDebugString(World, L.ToLocation + FVector(0, 0, 60), FString::Printf(TEXT("%d"), L.Depth), nullptr, FColor::White, 0.f, true, 1.5f);
		}
	}
}
