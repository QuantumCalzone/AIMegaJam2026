#include "Core/ChallengeDefinition.h"

UChallengeDefinition::UChallengeDefinition()
{
	SceneName = TEXT("Scene 3: The Stunt");
	ObjectiveText = TEXT("Smash the $2M Hero Camera at the end of a 3+ link chain.");
	AvailableItems = { ECartItem::BananaPeel, ECartItem::BowlingBall, ECartItem::Skateboard, ECartItem::ExtensionCord };
}
