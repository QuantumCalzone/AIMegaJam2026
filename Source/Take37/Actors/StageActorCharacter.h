#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Chain/PropVisuals.h"
#include "StageActorCharacter.generated.h"

class UAnimationAsset;
class UChainPropComponent;
class UActorBrainComponent;
class UStaticMeshComponent;

/** One stop on an actor's blocking route. */
struct FRouteStep
{
	FVector Mark = FVector::ZeroVector;
	float Wait = 1.f;
	float Speed = 140.f;
};

/** Personality (GDD section 6.2). All 0..1. */
struct FActorTraits
{
	float Bravado = 0.f;
	float Drama = 0.f;
	float Panic = 0.f;
	float Helpfulness = 0.f;
	float Clumsiness = 0.f;
	float Vanity = 0.f;
	FString GrudgeTarget;   // display name of the actor this one blames
	float Grudge = 0.f;
};

struct FStageActorSpec
{
	FString Id;
	FString BarkId;   // speaker name in DT_Barks
	FString Name;
	FString Role;
	FLinearColor Color = FLinearColor::White;
	FLinearColor Skin = FLinearColor(0.95f, 0.7f, 0.55f);
	float Scale = 1.f;
	FActorTraits Traits;
	TArray<FRouteStep> Route;
};

/**
 * Cast member: the UE mannequin tinted per character with costume pieces (GDD section 9.2 fallback). Walks its
 * blocking route, and its brain makes it react to chaos with ragdolls, dives, panic runs and shoves.
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

	// --- Actions the brain can trigger ---
	void DoFace(const FVector& Target);
	void DoHop();
	void DoRecoil(const FVector& AwayFrom, float Duration);
	void DoPanicRun(float Duration);
	void DoRagdoll(const FVector& VelocityChange);
	void DoDive(const FVector& Target);
	void DoPose(float Duration);
	void DoShove(AStageActorCharacter* Target);
	void DoStormOff();

	bool IsBusy() const { return State == EState::Acting || State == EState::Down || State == EState::Out; }
	bool IsDown() const { return State == EState::Down; }
	bool IsOut() const { return State == EState::Out; }
	void Bark(const TCHAR* Tag, int32 MinIntensity = 0);

	FString DisplayName;
	FString Role;
	FStageActorSpec Spec;
	UChainPropComponent* GetChainProp() const { return ChainProp; }

private:
	enum class EState : uint8 { Idle, Moving, Waiting, Done, Acting, Down, Out };
	enum class EAction : uint8 { None, Face, Hop, Recoil, Panic, Dive, Pose, Shove, StormOff };

	void BuildCostume();
	void UpdateAnimation(float Speed);
	void EndAction();
	void GetUp();
	void ForceStand(const FVector& Location);
	void SetSkirtVisible(bool bVisible);

	UFUNCTION()
	void OnMeshHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit);

	FTransform StartTransform;
	EState State = EState::Idle;
	EState ReturnState = EState::Idle;
	EAction Action = EAction::None;
	int32 StepIndex = 0;
	float WaitTimer = 0.f;
	float ActionTimer = 0.f;
	float DownTime = 0.f;
	float CalmTime = 0.f;
	float PanicRedirect = 0.f;
	FVector ActionDir = FVector::ZeroVector;
	TWeakObjectPtr<AStageActorCharacter> ShoveTarget;

	TArray<FVisualPart> Parts;
	TArray<UStaticMeshComponent*> SkirtParts;
	UPROPERTY() TObjectPtr<UAnimationAsset> IdleAnim;
	UPROPERTY() TObjectPtr<UAnimationAsset> WalkAnim;
	UPROPERTY() TObjectPtr<UAnimationAsset> RunAnim;
	UPROPERTY() TObjectPtr<UAnimationAsset> HopAnim;
	UPROPERTY() TObjectPtr<UChainPropComponent> ChainProp;
	UPROPERTY() TObjectPtr<UActorBrainComponent> Brain;
	int32 CurrentAnim = -1;
};
