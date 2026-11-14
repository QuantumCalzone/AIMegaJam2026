#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Chain/PropVisuals.h"
#include "StageActorCharacter.generated.h"

class UAnimationAsset;
class UChainPropComponent;

/** One stop on an actor's blocking route. */
struct FRouteStep
{
	FVector Mark = FVector::ZeroVector;
	float Wait = 1.f;
	float Speed = 140.f;
};

struct FStageActorSpec
{
	FString Id;
	FString Name;
	FString Role;
	FLinearColor Color = FLinearColor::White;
	FLinearColor Skin = FLinearColor(0.95f, 0.7f, 0.55f);
	float Scale = 1.f;
	TArray<FRouteStep> Route;
};

/**
 * Placeholder cast member: the UE mannequin tinted per character with costume pieces (GDD section 9.2 fallback),
 * walking its blocking route with idle/walk/run animation. Generated models replace the mesh later.
 */
UCLASS()
class TAKE37_API AStageActorCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AStageActorCharacter();

	void Setup(const FStageActorSpec& InSpec);
	void StartRoute();
	void ResetToStart();

	virtual void Tick(float DeltaTime) override;

	FString DisplayName;
	FString Role;

private:
	enum class EState : uint8 { Idle, Moving, Waiting, Done };

	void BuildCostume();
	void UpdateAnimation(float Speed);

	FStageActorSpec Spec;
	FTransform StartTransform;
	EState State = EState::Idle;
	int32 StepIndex = 0;
	float WaitTimer = 0.f;

	TArray<FVisualPart> Parts;
	UPROPERTY() TObjectPtr<UAnimationAsset> IdleAnim;
	UPROPERTY() TObjectPtr<UAnimationAsset> WalkAnim;
	UPROPERTY() TObjectPtr<UAnimationAsset> RunAnim;
	UPROPERTY() TObjectPtr<UChainPropComponent> ChainProp;
	int32 CurrentAnim = -1;
};
