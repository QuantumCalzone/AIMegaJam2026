#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Chain/ChainTypes.h"
#include "Chain/PropVisuals.h"
#include "Take37PropActor.generated.h"

class UShapeComponent;
class UChainPropComponent;

/** Everything needed to build a prop: collision shape, composite model and chain data. */
struct FPropSpec
{
	/** Collision shape: Cube (box), Sphere, Cylinder or Cone (capsule when taller than wide, else box). */
	FString Shape = TEXT("Cube");
	/** Model to build. Empty means a single Shape mesh. */
	FString Kind;
	/** Full dimensions in metres (1.0 = 100 cm). */
	FVector Scale = FVector(1.0);
	FLinearColor Color = FLinearColor(0.6f, 0.6f, 0.6f);
	FString Name;
	bool bDynamic = false;
	bool bTracked = false;
	float MassKg = 10.f;
	EChainCategory Category = EChainCategory::Furniture;
	float Value = 100.f;
	float Dollars = 0.f;
	float MinImpulse = 1500.f;
	bool bExpensive = false;
	bool bCanOrigin = false;
	bool bMovable = false;
	float MoveRadius = 200.f;
	bool bSimulateInTake = true;
};

/** A stage prop, placed item or set piece. Collision is a simple shape; the look is a composite model. */
UCLASS()
class TAKE37_API ATake37PropActor : public AActor
{
	GENERATED_BODY()

public:
	ATake37PropActor();

	UPROPERTY() TObjectPtr<UShapeComponent> Body;
	UPROPERTY() TObjectPtr<UChainPropComponent> ChainProp;

	FPropSpec Spec;
	FTransform Home;
	bool bPlacedByPlayer = false;
	int32 CartCost = 0;

	void Configure(const FPropSpec& InSpec);

	void SetPhysicsActive(bool bActive);
	void SaveHome() { Home = GetActorTransform(); }
	void ResetToHome();
	void SetGhost();
	void SetTint(const FLinearColor& Color);
	void SetHighlight(bool bOn);

private:
	TArray<FVisualPart> Visuals;
};
