#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "Subsystems/WorldSubsystem.h"
#include "BarkSubsystem.generated.h"

/** Row of DT_Barks. Columns match Tools/barks/DT_Barks.csv (GDD section 10.2). */
USTRUCT(BlueprintType)
struct FBarkRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Actor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Tag;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Genre;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Intensity = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Subtitle;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Delivery;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString File;
};

DECLARE_MULTICAST_DELEGATE_ThreeParams(FOnBark, FName /*Actor*/, const FString& /*Subtitle*/, int32 /*Intensity*/);

/**
 * Picks pre-generated voice lines by actor + tag, avoiding repeats and spam (GDD section 6.5).
 * Plays /Game/Audio/VO/<Actor>/<Row>.<Row> when the sound asset exists; always emits the subtitle.
 */
UCLASS()
class TAKE37_API UBarkSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	virtual bool DoesSupportWorldType(const EWorldType::Type WorldType) const override;

	/** Returns true when a line was chosen. */
	bool RequestBark(FName Actor, FName Tag, int32 MinIntensity = 0);

	void SetGenre(FName InGenre) { Genre = InGenre; }

	FOnBark OnBark;

private:
	UDataTable* GetTable();

	UPROPERTY() TObjectPtr<UDataTable> Table;
	bool bTriedLoad = false;
	FName Genre = TEXT("Western");
	TMap<FName, TArray<FName>> Recent;
	TMap<FName, double> NextAllowed;
	double GlobalBusyUntil = 0.0;
	int32 GlobalBusyIntensity = 0;
};
