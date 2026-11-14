#include "AI/BarkSubsystem.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/PackageName.h"
#include "Sound/SoundBase.h"
#include "Take37.h"

static constexpr double BarkActorCooldown = 2.5;
static constexpr double BarkGlobalWindow = 1.0;

bool UBarkSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
	return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}

UDataTable* UBarkSubsystem::GetTable()
{
	if (!bTriedLoad)
	{
		bTriedLoad = true;
		if (FPackageName::DoesPackageExist(TEXT("/Game/Data/DT_Barks")))
		{
			Table = LoadObject<UDataTable>(nullptr, TEXT("/Game/Data/DT_Barks.DT_Barks"));
		}
		if (!Table)
		{
			UE_LOG(LogTake37, Warning, TEXT("DT_Barks not found at /Game/Data/DT_Barks. Run Tools/barks/import_barks.py. Barks are disabled."));
		}
	}
	return Table;
}

bool UBarkSubsystem::RequestBark(FName Actor, FName Tag, int32 MinIntensity)
{
	UDataTable* DT = GetTable();
	UWorld* World = GetWorld();
	if (!DT || !World)
	{
		return false;
	}

	const double Now = World->GetRealTimeSeconds();
	const bool bShriek = (Tag == TEXT("Panic"));

	if (const double* Next = NextAllowed.Find(Actor))
	{
		if (Now < *Next)
		{
			return false;
		}
	}
	// Only one actor speaks at a time, unless this line is more intense than the one playing or is a shriek.
	if (Now < GlobalBusyUntil && !bShriek && MinIntensity <= GlobalBusyIntensity)
	{
		return false;
	}

	TArray<TPair<FName, const FBarkRow*>> GenreMatches;
	TArray<TPair<FName, const FBarkRow*>> AnyMatches;
	const TArray<FName>& Recents = Recent.FindOrAdd(Actor);

	DT->ForeachRow<FBarkRow>(TEXT("BarkSubsystem"), [&](const FName& Key, const FBarkRow& Row)
	{
		if (Row.Actor != Actor || Row.Tag != Tag || Row.Intensity < MinIntensity || Recents.Contains(Key))
		{
			return;
		}
		if (Row.Genre == Genre)
		{
			GenreMatches.Emplace(Key, &Row);
		}
		else if (Row.Genre == TEXT("Any"))
		{
			AnyMatches.Emplace(Key, &Row);
		}
	});

	const TArray<TPair<FName, const FBarkRow*>>& Pool = GenreMatches.Num() > 0 ? GenreMatches : AnyMatches;
	if (Pool.Num() == 0)
	{
		return false;
	}

	const TPair<FName, const FBarkRow*>& Pick = Pool[FMath::RandRange(0, Pool.Num() - 1)];
	const FBarkRow& Row = *Pick.Value;

	TArray<FName>& History = Recent.FindOrAdd(Actor);
	History.Add(Pick.Key);
	if (History.Num() > 3)
	{
		History.RemoveAt(0);
	}
	NextAllowed.Add(Actor, Now + BarkActorCooldown);
	GlobalBusyUntil = Now + BarkGlobalWindow;
	GlobalBusyIntensity = Row.Intensity;

	const FString PackagePath = FString::Printf(TEXT("/Game/Audio/VO/%s/%s"), *Actor.ToString(), *Pick.Key.ToString());
	if (FPackageName::DoesPackageExist(PackagePath))
	{
		if (USoundBase* Sound = LoadObject<USoundBase>(nullptr, *(PackagePath + TEXT(".") + Pick.Key.ToString())))
		{
			UGameplayStatics::PlaySound2D(this, Sound);
		}
	}

	UE_LOG(LogTake37, Log, TEXT("Bark %s: \"%s\""), *Pick.Key.ToString(), *Row.Subtitle);
	OnBark.Broadcast(Actor, Row.Subtitle, Row.Intensity);
	return true;
}
