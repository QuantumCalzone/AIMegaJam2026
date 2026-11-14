#include "Player/PlacementComponent.h"
#include "Chain/CueDeviceActor.h"
#include "Chain/Take37PropActor.h"
#include "Core/CartCatalog.h"
#include "Core/ChallengeDefinition.h"
#include "Core/Take37Stage.h"
#include "Core/TakeDirectorSubsystem.h"
#include "UI/Take37HUD.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Take37.h"

UPlacementComponent::UPlacementComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

ATake37Stage* UPlacementComponent::FindStage() const
{
	for (TActorIterator<ATake37Stage> It(GetWorld()); It; ++It)
	{
		return *It;
	}
	return nullptr;
}

int32 UPlacementComponent::GetBudget() const
{
	const UTakeDirectorSubsystem* Dir = GetWorld() ? GetWorld()->GetSubsystem<UTakeDirectorSubsystem>() : nullptr;
	return (Dir && Dir->GetChallenge()) ? Dir->GetChallenge()->SabotageBudget : 1000;
}

bool UPlacementComponent::TraceCursor(APlayerController* PC, FHitResult& Out, AActor* Ignore) const
{
	FVector Origin, Dir;
	if (!PC || !PC->DeprojectMousePositionToWorld(Origin, Dir))
	{
		return false;
	}
	FCollisionQueryParams Params(SCENE_QUERY_STAT(Take37Cursor), false);
	if (Ignore)
	{
		Params.AddIgnoredActor(Ignore);
	}
	if (Ghost)
	{
		Params.AddIgnoredActor(Ghost);
	}
	return GetWorld()->LineTraceSingleByChannel(Out, Origin, Origin + Dir * 20000.0, ECC_Visibility, Params);
}

void UPlacementComponent::ToggleArmed(ECartItem Item)
{
	ClearSelection();
	Armed = (Armed == Item) ? ECartItem::None : Item;
	DestroyGhost();
}

void UPlacementComponent::DestroyGhost()
{
	if (Ghost)
	{
		Ghost->Destroy();
		Ghost = nullptr;
	}
}

void UPlacementComponent::ClearSelection()
{
	if (SelectedProp)
	{
		SelectedProp->SetHighlight(false);
	}
	if (ACueDeviceActor* D = SelectedDevice.Get())
	{
		D->SetHighlight(false);
	}
	SelectedProp = nullptr;
	SelectedDevice.Reset();
	bDragging = false;
}

void UPlacementComponent::SetSelection(ATake37PropActor* Prop, ACueDeviceActor* Device)
{
	ClearSelection();
	SelectedProp = Prop;
	SelectedDevice = Device;
	if (Prop)
	{
		Prop->SetHighlight(true);
	}
	if (Device)
	{
		Device->SetHighlight(true);
	}
}

bool UPlacementComponent::EvaluatePlacement(const FHitResult& Hit, FVector& OutLocation, FRotator& OutRotation, bool& bOutValid) const
{
	const FCartItemInfo& Info = Take37Cart::Get(Armed);
	const FVector HalfExtent = Info.Scale * 50.0;
	OutRotation = FRotator(0.f, GhostYaw, 0.f);
	OutLocation = Hit.ImpactPoint + FVector(0, 0, HalfExtent.Z + 0.5);

	bOutValid = Hit.bBlockingHit && Hit.ImpactNormal.Z > 0.7 && Info.Cost <= GetRemaining();
	// No stacking on top of simulated props.
	if (const ATake37PropActor* HitProp = Cast<ATake37PropActor>(Hit.GetActor()))
	{
		if (HitProp->Spec.bDynamic)
		{
			bOutValid = false;
		}
	}
	if (bOutValid)
	{
		const FVector Inset = (HalfExtent - FVector(3.0)).ComponentMax(FVector(1.0));
		FCollisionQueryParams Params(SCENE_QUERY_STAT(Take37PlaceTest), false);
		if (Ghost)
		{
			Params.AddIgnoredActor(Ghost);
		}
		bOutValid = !GetWorld()->OverlapAnyTestByChannel(OutLocation + FVector(0, 0, 3.0), OutRotation.Quaternion(), ECC_Visibility, FCollisionShape::MakeBox(Inset), Params);
	}
	return Hit.bBlockingHit;
}

void UPlacementComponent::UpdateGhost(APlayerController* PC)
{
	if (Armed == ECartItem::None)
	{
		DestroyGhost();
		return;
	}
	const FCartItemInfo& Info = Take37Cart::Get(Armed);
	if (!Ghost)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		Ghost = GetWorld()->SpawnActor<ATake37PropActor>(FVector(0, 0, -5000), FRotator::ZeroRotator, Params);
		if (Ghost)
		{
			FPropSpec S;
			S.Name = Info.Name;
			S.Shape = Info.Shape;
			S.Kind = Info.Kind;
			S.Scale = Info.Scale;
			S.Color = Info.Color;
			Ghost->Configure(S);
			Ghost->SetGhost();
		}
	}
	if (!Ghost)
	{
		return;
	}

	// Hide the ghost while the cursor is over a HUD button.
	if (const ATake37HUD* HUD = PC ? Cast<ATake37HUD>(PC->GetHUD()) : nullptr)
	{
		float X, Y;
		if (PC->GetMousePosition(X, Y) && HUD->HitTestButton(FVector2D(X, Y)) != NAME_None)
		{
			Ghost->SetActorHiddenInGame(true);
			return;
		}
	}

	FHitResult Hit;
	if (!TraceCursor(PC, Hit, nullptr))
	{
		Ghost->SetActorHiddenInGame(true);
		return;
	}
	FVector Loc;
	FRotator Rot;
	bool bValid = false;
	EvaluatePlacement(Hit, Loc, Rot, bValid);
	Ghost->SetActorHiddenInGame(false);
	Ghost->SetActorLocationAndRotation(Loc, Rot);
	Ghost->SetTint(bValid ? FLinearColor(0.1f, 1.f, 0.2f) : FLinearColor(1.f, 0.1f, 0.1f));
}

void UPlacementComponent::UpdateDrag(APlayerController* PC)
{
	if (!bDragging || !SelectedProp)
	{
		return;
	}
	FHitResult Hit;
	if (!TraceCursor(PC, Hit, SelectedProp) || Hit.ImpactNormal.Z < 0.7)
	{
		return;
	}
	FVector Origin, Extent;
	SelectedProp->GetActorBounds(false, Origin, Extent);
	FVector Target = Hit.ImpactPoint + FVector(0, 0, Extent.Z + 0.5);
	if (!SelectedProp->bPlacedByPlayer)
	{
		// Movable set dressing stays near where it was (GDD section 2.1).
		const FVector Home = SelectedProp->Home.GetLocation();
		FVector Flat = Target - Home;
		Flat.Z = 0.0;
		if (Flat.Size() > SelectedProp->Spec.MoveRadius)
		{
			Flat = Flat.GetSafeNormal() * SelectedProp->Spec.MoveRadius;
		}
		Target = FVector(Home.X + Flat.X, Home.Y + Flat.Y, Target.Z);
	}
	SelectedProp->SetActorLocation(Target, false, nullptr, ETeleportType::TeleportPhysics);
	SelectedProp->SaveHome();
}

void UPlacementComponent::TickPlacement(APlayerController* PC, float DeltaTime)
{
	const UTakeDirectorSubsystem* Dir = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>();
	if (!Dir || Dir->GetPhase() != ETake37Phase::Setup)
	{
		DestroyGhost();
		if (SelectedProp || SelectedDevice.IsValid())
		{
			ClearSelection();
		}
		Armed = ECartItem::None;
		return;
	}
	UpdateGhost(PC);
	UpdateDrag(PC);
}

void UPlacementComponent::PrimaryPressed(APlayerController* PC)
{
	FHitResult Hit;
	if (Armed != ECartItem::None)
	{
		if (!TraceCursor(PC, Hit, nullptr))
		{
			return;
		}
		FVector Loc;
		FRotator Rot;
		bool bValid = false;
		EvaluatePlacement(Hit, Loc, Rot, bValid);
		if (!bValid)
		{
			return;
		}
		ATake37Stage* Stage = FindStage();
		if (!Stage)
		{
			return;
		}
		const FCartItemInfo& Info = Take37Cart::Get(Armed);
		FPropSpec S;
		S.Name = Info.Name;
		S.Shape = Info.Shape;
		S.Kind = Info.Kind;
		S.Scale = Info.Scale;
		S.Color = Info.Color;
		S.bDynamic = true;
		S.bTracked = true;
		S.MassKg = Info.MassKg;
		S.Category = Info.Category;
		S.Value = Info.Value;
		S.MinImpulse = Info.MinImpulse;
		S.bCanOrigin = Info.bCanOrigin;
		if (ATake37PropActor* Prop = Stage->SpawnProp(S, Loc, Rot, true))
		{
			Prop->bPlacedByPlayer = true;
			Prop->CartCost = Info.Cost;
			Spent += Info.Cost;
			UE_LOG(LogTake37, Log, TEXT("Placed %s ($%d). Budget left $%d"), *Info.Name, Info.Cost, GetRemaining());
		}
		return;
	}

	// Select what is under the cursor.
	if (!TraceCursor(PC, Hit, nullptr))
	{
		ClearSelection();
		return;
	}
	if (ACueDeviceActor* Device = Cast<ACueDeviceActor>(Hit.GetActor()))
	{
		SetSelection(nullptr, Device);
	}
	else if (ATake37PropActor* Prop = Cast<ATake37PropActor>(Hit.GetActor()))
	{
		if (Prop->bPlacedByPlayer || Prop->Spec.bMovable)
		{
			SetSelection(Prop, nullptr);
			bDragging = true;
		}
		else
		{
			ClearSelection();
		}
	}
	else
	{
		ClearSelection();
	}
}

void UPlacementComponent::PrimaryReleased()
{
	bDragging = false;
}

void UPlacementComponent::RotateSelected(float Degrees)
{
	if (Armed != ECartItem::None)
	{
		GhostYaw += Degrees;
	}
	else if (SelectedProp)
	{
		SelectedProp->AddActorWorldRotation(FRotator(0.f, Degrees, 0.f), false, nullptr, ETeleportType::TeleportPhysics);
		SelectedProp->SaveHome();
	}
}

void UPlacementComponent::DeleteSelected()
{
	if (Armed != ECartItem::None)
	{
		Armed = ECartItem::None;
		DestroyGhost();
		return;
	}
	if (SelectedProp && SelectedProp->bPlacedByPlayer)
	{
		Spent = FMath::Max(0, Spent - SelectedProp->CartCost);
		if (ATake37Stage* Stage = FindStage())
		{
			Stage->UnregisterProp(SelectedProp);
		}
		ATake37PropActor* ToDestroy = SelectedProp;
		ClearSelection();
		ToDestroy->Destroy();
	}
}
