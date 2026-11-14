#pragma once

#include "CoreMinimal.h"
#include "ChainTypes.generated.h"

UENUM(BlueprintType)
enum class EChainCategory : uint8
{
	Furniture,
	Lighting,
	Camera,
	Food,
	Liquid,
	Hazard,
	Effect,
	Actor,
};

UENUM(BlueprintType)
enum class EChainLinkType : uint8
{
	Origin,
	Collision,
	Trigger,
	Cue,
};

UENUM(BlueprintType)
enum class ETakeEventType : uint8
{
	Link,
	Cue,
	Bark,
	Phase,
};

/** One edge in the causal graph (GDD section 4.2). */
USTRUCT(BlueprintType)
struct FChainLink
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly) int32 ChainId = INDEX_NONE;
	UPROPERTY(BlueprintReadOnly) FName FromName;
	UPROPERTY(BlueprintReadOnly) FName ToName;
	UPROPERTY(BlueprintReadOnly) int32 Depth = 0;
	UPROPERTY(BlueprintReadOnly) float Impulse = 0.f;
	UPROPERTY(BlueprintReadOnly) float Time = 0.f;
	UPROPERTY(BlueprintReadOnly) FVector FromLocation = FVector::ZeroVector;
	UPROPERTY(BlueprintReadOnly) FVector ToLocation = FVector::ZeroVector;
	UPROPERTY(BlueprintReadOnly) EChainLinkType LinkType = EChainLinkType::Collision;
	UPROPERTY(BlueprintReadOnly) EChainCategory ToCategory = EChainCategory::Furniture;
	UPROPERTY(BlueprintReadOnly) bool bImprov = false;
	UPROPERTY(BlueprintReadOnly) float Score = 0.f;
	UPROPERTY(BlueprintReadOnly) float ComboMultiplier = 1.f;
};

/** Ordered log entry; feeds the highlight picker, critic prompt and score card (GDD section 4.4). */
USTRUCT(BlueprintType)
struct FTakeEvent
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly) float Time = 0.f;
	UPROPERTY(BlueprintReadOnly) ETakeEventType Type = ETakeEventType::Link;
	UPROPERTY(BlueprintReadOnly) FString Text;
	UPROPERTY(BlueprintReadOnly) float Score = 0.f;
	UPROPERTY(BlueprintReadOnly) int32 ChainId = INDEX_NONE;
};

DECLARE_MULTICAST_DELEGATE_OneParam(FOnChainLink, const FChainLink&);
DECLARE_MULTICAST_DELEGATE(FOnScoreChanged);
