#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "InputActionValue.h"
#include "Core/Take37Types.h"
#include "DirectorPawn.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UInputAction;
class UInputMappingContext;
class UPlacementComponent;

/**
 * Setup-phase orbit camera, placement and cue input (GDD sections 5.1 and 8.1).
 * Input actions and the mapping context are built in code so the project needs no input assets.
 */
UCLASS()
class TAKE37_API ADirectorPawn : public APawn
{
	GENERATED_BODY()

public:
	ADirectorPawn();

	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

	UPlacementComponent* GetPlacement() const { return Placement; }

protected:
	virtual void BeginPlay() override;

private:
	void BuildInput();
	void OnMove(const FInputActionValue& Value);
	void OnMoveCompleted();
	void OnZoom(const FInputActionValue& Value);
	void OnOrbitStarted() { bOrbit = true; }
	void OnOrbitCompleted() { bOrbit = false; }
	void OnPrimaryStarted();
	void OnPrimaryCompleted();
	void OnRotate(const FInputActionValue& Value);
	void OnDelete();
	void OnCue(int32 Slot);
	void OnActionKey();

	void HandleButton(FName Button);

	UPROPERTY(VisibleAnywhere) TObjectPtr<USceneComponent> Root;
	UPROPERTY(VisibleAnywhere) TObjectPtr<USpringArmComponent> Arm;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UCameraComponent> Camera;
	UPROPERTY(VisibleAnywhere) TObjectPtr<UPlacementComponent> Placement;

	UPROPERTY() TObjectPtr<UInputMappingContext> Context;
	UPROPERTY() TObjectPtr<UInputAction> MoveAction;
	UPROPERTY() TObjectPtr<UInputAction> ZoomAction;
	UPROPERTY() TObjectPtr<UInputAction> OrbitAction;
	UPROPERTY() TObjectPtr<UInputAction> PrimaryAction;
	UPROPERTY() TObjectPtr<UInputAction> RotateAction;
	UPROPERTY() TObjectPtr<UInputAction> DeleteAction;
	UPROPERTY() TObjectPtr<UInputAction> ActionAction;
	UPROPERTY() TArray<TObjectPtr<UInputAction>> CueActions;

	FVector2D MoveInput = FVector2D::ZeroVector;
	bool bOrbit = false;
	bool bHasLastMouse = false;
	FVector2D LastMouse = FVector2D::ZeroVector;

	float Yaw = 90.f;
	float Pitch = -52.f;
	float ArmLength = 2300.f;
	FVector Pivot = FVector(0.0, -60.0, 0.0);
};
