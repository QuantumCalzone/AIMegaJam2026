#pragma once

#include "CoreMinimal.h"
#include "Take37Types.generated.h"

/** Round phases: Setup -> Take -> Cut -> Results (GDD section 2). */
UENUM(BlueprintType)
enum class ETake37Phase : uint8
{
	Setup,
	Take,
	Cut,
	Results,
};

/** Placeable sabotage items on the Prop Cart (GDD section 5.2). M1 ships the first four. */
UENUM(BlueprintType)
enum class ECartItem : uint8
{
	None,
	BananaPeel,
	BowlingBall,
	Skateboard,
	ExtensionCord,
};
