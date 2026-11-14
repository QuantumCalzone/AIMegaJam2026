#include "Core/TakeDirectorSubsystem.h"
#include "AI/BarkSubsystem.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Chain/CueDeviceActor.h"
#include "Core/ChallengeDefinition.h"
#include "Core/ScoringConfig.h"
#include "Core/Take37Stage.h"
#include "Engine/World.h"
#include "HAL/PlatformTime.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"
#include "Take37.h"

bool UTakeDirectorSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
	return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}

TStatId UTakeDirectorSubsystem::GetStatId() const
{
	RETURN_QUICK_DECLARE_CYCLE_STAT(UTakeDirectorSubsystem, STATGROUP_Tickables);
}

void UTakeDirectorSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Collection.InitializeDependency<UChainReactionSubsystem>();
	Collection.InitializeDependency<UBarkSubsystem>();
	Super::Initialize(Collection);

	Challenge = NewObject<UChallengeDefinition>(this, TEXT("DefaultChallenge"));
	CueSlots.SetNum(NumCueSlots);
	Chain = GetWorld()->GetSubsystem<UChainReactionSubsystem>();
	Barks = GetWorld()->GetSubsystem<UBarkSubsystem>();
	if (Chain.IsValid())
	{
		Chain->OnLink.AddUObject(this, &UTakeDirectorSubsystem::HandleLink);
	}
	if (Barks.IsValid())
	{
		Barks->SetGenre(Challenge->Genre);
	}
}

void UTakeDirectorSubsystem::Deinitialize()
{
	if (Chain.IsValid())
	{
		Chain->OnLink.RemoveAll(this);
	}
	Super::Deinitialize();
}

float UTakeDirectorSubsystem::GetTakeTimeLimit() const
{
	return Challenge ? Challenge->TakeTimeLimit : 45.f;
}

void UTakeDirectorSubsystem::Bark(FName Actor, FName Tag, int32 MinIntensity)
{
	if (Barks.IsValid())
	{
		Barks->RequestBark(Actor, Tag, MinIntensity);
	}
}

void UTakeDirectorSubsystem::SetPhase(ETake37Phase NewPhase)
{
	const ETake37Phase Old = Phase;
	Phase = NewPhase;
	PhaseTime = 0.f;
	UE_LOG(LogTake37, Log, TEXT("Phase %d -> %d"), static_cast<int32>(Old), static_cast<int32>(NewPhase));
	OnPhaseChanged.Broadcast(Old, NewPhase);
}

void UTakeDirectorSubsystem::AssignCue(int32 Slot, ACueDeviceActor* Device)
{
	if (!CueSlots.IsValidIndex(Slot))
	{
		return;
	}
	// A device lives in one slot at a time.
	for (TWeakObjectPtr<ACueDeviceActor>& S : CueSlots)
	{
		if (S.Get() == Device)
		{
			S.Reset();
		}
	}
	CueSlots[Slot] = Device;
}

ACueDeviceActor* UTakeDirectorSubsystem::GetCueDevice(int32 Slot) const
{
	return CueSlots.IsValidIndex(Slot) ? CueSlots[Slot].Get() : nullptr;
}

void UTakeDirectorSubsystem::StartSetup()
{
	if (Chain.IsValid())
	{
		Chain->ResetTake();
	}
	TakeTime = 0.f;
	SetPhase(ETake37Phase::Setup);
	Bark(TEXT("Director"), TEXT("Setup"));
}

void UTakeDirectorSubsystem::RequestAction()
{
	if (Phase != ETake37Phase::Setup || !Chain.IsValid())
	{
		return;
	}
	TakeTime = 0.f;
	Chain->ResetTake();
	Chain->BeginTake();
	SetPhase(ETake37Phase::Take);
	if (Barks.IsValid())
	{
		Barks->RequestBark(TEXT("Director"), TEXT("Action"));
	}
}

bool UTakeDirectorSubsystem::FireCue(int32 Slot)
{
	if (Phase != ETake37Phase::Take)
	{
		return false;
	}
	ACueDeviceActor* Device = GetCueDevice(Slot);
	if (!Device || Device->bFired)
	{
		return false;
	}
	Device->Fire();
	return true;
}

void UTakeDirectorSubsystem::RequestCut()
{
	if (Phase == ETake37Phase::Take && TakeTime >= 5.f)
	{
		EndTake(TEXT("director skipped to CUT"));
	}
}

void UTakeDirectorSubsystem::RequestRetry()
{
	if (Phase == ETake37Phase::Results)
	{
		++TakeNumber;
		StartSetup();
		Bark(TEXT("Director"), TEXT("Retry"));
	}
}

void UTakeDirectorSubsystem::EndTake(const TCHAR* Reason)
{
	UE_LOG(LogTake37, Log, TEXT("CUT: %s (take time %.1f s)"), Reason, TakeTime);
	if (Chain.IsValid())
	{
		Chain->EndTake();
	}
	SetPhase(ETake37Phase::Cut);
	Bark(TEXT("Director"), TEXT("Cut"));
}

void UTakeDirectorSubsystem::ShowResults()
{
	BuildResults();
	SetPhase(ETake37Phase::Results);
}

void UTakeDirectorSubsystem::Tick(float DeltaTime)
{
	// Hit-stop is timed in real time so it is not stretched by its own time dilation.
	if (bHitStopActive && FPlatformTime::Seconds() >= HitStopEndsReal)
	{
		bHitStopActive = false;
		UGameplayStatics::SetGlobalTimeDilation(this, 1.f);
	}

	PhaseTime += DeltaTime;
	switch (Phase)
	{
	case ETake37Phase::Take:
	{
		TakeTime += DeltaTime;
		if (!Chain.IsValid())
		{
			break;
		}
		const float WorldNow = GetWorld()->GetTimeSeconds();
		const bool bAnyLink = Chain->GetLinkCount() > 0;
		const float Quiet = WorldNow - FMath::Max(Chain->GetLastLinkTime(), Chain->GetTakeStartTime());
		if (TakeTime >= GetTakeTimeLimit())
		{
			EndTake(TEXT("time limit"));
		}
		else if (bAnyLink && TakeTime > 4.f && Quiet > 4.f)
		{
			EndTake(TEXT("4 s without new events"));
		}
		else if (!bAnyLink && TakeTime > 15.f)
		{
			EndTake(TEXT("nothing happened"));
		}
		break;
	}
	case ETake37Phase::Cut:
		if (bHitStopActive)
		{
			bHitStopActive = false;
			UGameplayStatics::SetGlobalTimeDilation(this, 1.f);
		}
		if (PhaseTime >= 2.5f)
		{
			ShowResults();
		}
		break;
	default:
		break;
	}
}

void UTakeDirectorSubsystem::HandleLink(const FChainLink& Link)
{
	if (Phase != ETake37Phase::Take || !Chain.IsValid() || !Chain->GetConfig())
	{
		return;
	}
	const UScoringConfig* Config = Chain->GetConfig();
	const double RealNow = FPlatformTime::Seconds();
	if (Link.Impulse >= Config->BigHitImpulse && (RealNow - LastHitStopReal) >= Config->HitStopCooldown)
	{
		LastHitStopReal = RealNow;
		HitStopEndsReal = RealNow + Config->HitStopDuration;
		bHitStopActive = true;
		UGameplayStatics::SetGlobalTimeDilation(this, Config->HitStopDilation);
	}
	if (Link.ToCategory == EChainCategory::Camera)
	{
		Bark(TEXT("FirstAD"), TEXT("Damage"), 2);
	}
}

namespace
{
	FString FormatCount(int64 Value)
	{
		return FText::AsNumber(Value).ToString();
	}

	const FString& PickFrom(const TArray<FString>& Options, int32 Seed)
	{
		return Options[FMath::Abs(Seed) % Options.Num()];
	}
}

void UTakeDirectorSubsystem::BuildResults()
{
	Results = FTakeResults();
	if (!Chain.IsValid() || !Challenge)
	{
		return;
	}

	Results.Score = FMath::RoundToInt64(Chain->GetTotalScore());
	Results.Damages = static_cast<int64>(Chain->GetDamages());
	Results.BestChain = Chain->GetBestChainLinks();
	Results.LinkCount = Chain->GetLinkCount();
	Results.bHeroHit = Chain->WasHeroCameraHit();
	Results.HeroDepth = Chain->GetHeroCameraDepth();

	// Stars are deterministic and come from score, never from a language model (GDD section 7.3).
	const bool bStar1 = Results.bHeroHit && Results.HeroDepth >= Challenge->MinChainForObjective;
	const bool bStar2 = bStar1 && Results.Score >= Challenge->Star2Score;
	const bool bStar3 = bStar2 && Results.BestChain >= Challenge->Star3Chain;
	Results.Stars = bStar3 ? 3 : (bStar2 ? 2 : (bStar1 ? 1 : 0));

	float BestScore = -1.f;
	for (const FChainLink& L : Chain->GetLinks())
	{
		if (L.LinkType != EChainLinkType::Origin && L.Score > BestScore)
		{
			BestScore = L.Score;
			Results.TopLink = L.ToName.ToString();
		}
	}
	if (Results.TopLink.IsEmpty())
	{
		Results.TopLink = TEXT("thin air");
	}

	// Canned critic review (the LLM version replaces this later; GDD section 7.3 fallback).
	const TArray<FString> Critics = { TEXT("Mabel Quill"), TEXT("Thaddeus Frame"), TEXT("Rex Montage") };
	const TArray<FString> Papers = { TEXT("The Daily Clapper"), TEXT("Reel Talk Weekly") };
	Results.CriticName = PickFrom(Critics, TakeNumber + Results.LinkCount);
	Results.Publication = PickFrom(Papers, TakeNumber);

	static const TArray<TArray<FString>> Headlines = {
		{ TEXT("Nothing Happens, Beautifully"), TEXT("A Quiet Day at the Studio") },
		{ TEXT("Mild Mayhem at High Noon"), TEXT("Collapse, Modestly Staged") },
		{ TEXT("A Tour-de-Force of Collapse"), TEXT("Chaos With a Plot") },
		{ TEXT("The Year's Boldest Disaster"), TEXT("Demolition, Directed") },
	};
	static const TArray<TArray<FString>> Reviews = {
		{ TEXT("The {top} did what it could with a {n}-link effort. The $2M camera lives to see another day. A pity.") },
		{ TEXT("A {n}-link chain, led by the {top}. The camera was threatened but never truly ruined. Damages: ${dmg}. Promising.") },
		{ TEXT("The {top} set off {n} links of splendid ruin, and the $2M camera took the final bow. ${dmg} in damages. Studio executives wept.") },
		{ TEXT("A {n}-link masterpiece. The {top} steals the scene, the camera meets its fate, and the insurance adjuster meets a nervous breakdown. ${dmg}!") },
	};
	static const TArray<TArray<FString>> Quotes = {
		{ TEXT("Where was the carnage?") },
		{ TEXT("Almost a disaster.") },
		{ TEXT("The camera never saw it coming.") },
		{ TEXT("Cinema will never recover.") },
	};

	const int32 S = FMath::Clamp(Results.Stars, 0, 3);
	Results.Headline = PickFrom(Headlines[S], TakeNumber);
	Results.Review = PickFrom(Reviews[S], 0)
		.Replace(TEXT("{top}"), *Results.TopLink)
		.Replace(TEXT("{n}"), *FString::FromInt(Results.BestChain))
		.Replace(TEXT("{dmg}"), *FormatCount(Results.Damages));
	Results.PullQuote = PickFrom(Quotes[S], 0);
}

// Debug commands (GDD section 12.5): drive the phase machine from the console or automated tests.
static FAutoConsoleCommandWithWorldAndArgs GT37Action(
	TEXT("t37.Action"), TEXT("Start the take (same as pressing ACTION!)."),
	FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>&, UWorld* World)
	{
		if (World)
		{
			if (UTakeDirectorSubsystem* Dir = World->GetSubsystem<UTakeDirectorSubsystem>())
			{
				Dir->RequestAction();
			}
		}
	}));

static FAutoConsoleCommandWithWorldAndArgs GT37Cue(
	TEXT("t37.Cue"), TEXT("t37.Cue <1-3>: fire a cue slot during a take."),
	FConsoleCommandWithWorldAndArgsDelegate::CreateLambda([](const TArray<FString>& Args, UWorld* World)
	{
		if (World && Args.Num() > 0)
		{
			if (UTakeDirectorSubsystem* Dir = World->GetSubsystem<UTakeDirectorSubsystem>())
			{
				Dir->FireCue(FCString::Atoi(*Args[0]) - 1);
			}
		}
	}));
