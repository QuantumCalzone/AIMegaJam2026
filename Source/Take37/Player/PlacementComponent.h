#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Core/Take37Types.h"
#include "PlacementComponent.generated.h"

class ATake37PropActor;
class ACueDeviceActor;
class ATake37Stage;

/** Ghost preview, validation, budget, selection and drag for the Setup phase (GDD section 5.1). */
UCLASS()
class TAKE37_API UPlacementComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UPlacementComponent();

	/** Called each frame by the pawn while it is possessed. */
	void TickPlacement(APlayerController* PC, float DeltaTime);

	void ToggleArmed(ECartItem Item);
	ECartItem GetArmed() const { return Armed; }

	/** Click in the world during Setup: place armed item, or select / start dragging what is under the cursor. */
	void PrimaryPressed(APlayerController* PC);
	void PrimaryReleased();
	void RotateSelected(float Degrees);
	/** Delete key: returns a placed item to the cart, or clears the armed item. */
	void DeleteSelected();

	ACueDeviceActor* GetSelectedDevice() const { return SelectedDevice.Get(); }
	int32 GetBudget() const;
	int32 GetSpent() const { return Spent; }
	int32 GetRemaining() const { return GetBudget() - Spent; }

private:
	ATake37Stage* FindStage() const;
	bool TraceCursor(APlayerController* PC, FHitResult& Out, AActor* Ignore) const;
	void ClearSelection();
	void SetSelection(ATake37PropActor* Prop, ACueDeviceActor* Device);
	void UpdateGhost(APlayerController* PC);
	void DestroyGhost();
	bool EvaluatePlacement(const FHitResult& Hit, FVector& OutLocation, FRotator& OutRotation, bool& bOutValid) const;
	void UpdateDrag(APlayerController* PC);

	ECartItem Armed = ECartItem::None;
	float GhostYaw = 0.f;
	int32 Spent = 0;

	UPROPERTY() TObjectPtr<ATake37PropActor> Ghost;
	UPROPERTY() TObjectPtr<ATake37PropActor> SelectedProp;
	TWeakObjectPtr<ACueDeviceActor> SelectedDevice;
	bool bDragging = false;
};
