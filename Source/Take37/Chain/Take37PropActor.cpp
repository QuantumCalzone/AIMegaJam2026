#include "Chain/Take37PropActor.h"
#include "Chain/ChainPropComponent.h"
#include "Components/BoxComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/ShapeComponent.h"
#include "Components/SphereComponent.h"
#include "Take37.h"

ATake37PropActor::ATake37PropActor()
{
	PrimaryActorTick.bCanEverTick = false;
	SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("TempRoot")));
}

void ATake37PropActor::Configure(const FPropSpec& InSpec)
{
	Spec = InSpec;
	const FTransform Start = GetActorTransform();
	const FVector Half = Spec.Scale * 50.0;

	// Collision shape becomes the root, so physics moves the whole actor.
	UShapeComponent* Shape = nullptr;
	if (Spec.Shape == TEXT("Sphere"))
	{
		USphereComponent* S = NewObject<USphereComponent>(this, TEXT("Body"));
		S->SetSphereRadius(Half.X, false);
		Shape = S;
	}
	else if ((Spec.Shape == TEXT("Cylinder") || Spec.Shape == TEXT("Cone")) && Half.Z >= Half.X)
	{
		UCapsuleComponent* C = NewObject<UCapsuleComponent>(this, TEXT("Body"));
		C->SetCapsuleSize(Half.X, Half.Z, false);
		Shape = C;
	}
	else
	{
		UBoxComponent* B = NewObject<UBoxComponent>(this, TEXT("Body"));
		B->SetBoxExtent(Half, false);
		Shape = B;
	}
	Body = Shape;
	Shape->SetMobility(EComponentMobility::Movable);
	Shape->SetHiddenInGame(true);
	Shape->SetGenerateOverlapEvents(false);
	Shape->SetCanEverAffectNavigation(false);
	Shape->SetCollisionProfileName(Spec.bDynamic ? TEXT("PhysicsActor") : TEXT("BlockAll"));

	USceneComponent* OldRoot = GetRootComponent();
	Shape->RegisterComponent();
	SetRootComponent(Shape);
	if (OldRoot)
	{
		OldRoot->DestroyComponent();
	}
	SetActorTransform(Start);

	if (Spec.bDynamic)
	{
		Shape->SetMassOverrideInKg(NAME_None, Spec.MassKg, true);
		Shape->SetSimulatePhysics(false);
	}

	const FString Kind = Spec.Kind.IsEmpty() ? Spec.Shape : Spec.Kind;
	Take37Visuals::Build(this, Shape, Visuals, Kind, Spec.Scale * 100.0, Spec.Color);

	if (Spec.bTracked)
	{
		ChainProp = NewObject<UChainPropComponent>(this, TEXT("ChainProp"));
		ChainProp->Category = Spec.Category;
		ChainProp->DisplayName = Spec.Name;
		ChainProp->BaseValue = Spec.Value;
		ChainProp->DollarValue = Spec.Dollars;
		ChainProp->MinImpulseToCount = Spec.MinImpulse;
		ChainProp->bExpensive = Spec.bExpensive;
		ChainProp->bCanOriginChain = Spec.bCanOrigin;
		ChainProp->RegisterComponent();
	}
	SaveHome();
}

void ATake37PropActor::SetPhysicsActive(bool bActive)
{
	if (!Spec.bDynamic || !Body)
	{
		return;
	}
	Body->SetSimulatePhysics(bActive);
	if (bActive)
	{
		Body->WakeAllRigidBodies();
	}
}

void ATake37PropActor::ResetToHome()
{
	if (Spec.bDynamic && Body)
	{
		Body->SetSimulatePhysics(false);
	}
	SetActorTransform(Home, false, nullptr, ETeleportType::TeleportPhysics);
	if (ChainProp)
	{
		ChainProp->ResetRuntime();
	}
}

void ATake37PropActor::SetGhost()
{
	if (Body)
	{
		Body->SetSimulatePhysics(false);
		Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

void ATake37PropActor::SetTint(const FLinearColor& Color)
{
	Take37Visuals::Tint(Visuals, &Color, 0.f);
}

void ATake37PropActor::SetHighlight(bool bOn)
{
	Take37Visuals::Tint(Visuals, nullptr, bOn ? 0.5f : 0.f);
}
