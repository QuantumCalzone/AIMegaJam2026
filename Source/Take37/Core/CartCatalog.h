#pragma once

#include "CoreMinimal.h"
#include "Core/Take37Types.h"
#include "Chain/ChainTypes.h"

/** Static description of a Prop Cart item (GDD section 5.2). */
struct FCartItemInfo
{
	FString Name;
	int32 Cost = 0;
	FString Shape = TEXT("Cube");
	FString Kind;
	FVector Scale = FVector(1.0);
	float MassKg = 1.f;
	FLinearColor Color = FLinearColor::White;
	EChainCategory Category = EChainCategory::Hazard;
	float Value = 100.f;
	float MinImpulse = 300.f;
	bool bCanOrigin = false;
};

namespace Take37Cart
{
	const FCartItemInfo& Get(ECartItem Item);
}
