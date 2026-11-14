#include "Chain/CueDeviceActor.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Chain/Take37PropActor.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Take37.h"

ACueDeviceActor::ACueDeviceActor()
{
	PrimaryActorTick.bCanEverTick = false;
	SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("TempRoot")));
}

void ACueDeviceActor::Setup(ECueType InType, const FString& InName, const FVector& Size, const FLinearColor& Color, const FString& Kind)
{
	CueType = InType;
	DisplayName = InName;

	const FTransform Start = GetActorTransform();
	Body = NewObject<UBoxComponent>(this, TEXT("Body"));
	Body->SetBoxExtent(Size * 50.0, false);
	Body->SetMobility(EComponentMobility::Movable);
	Body->SetHiddenInGame(true);
	Body->SetGenerateOverlapEvents(false);
	Body->SetCollisionProfileName(TEXT("BlockAll"));
	USceneComponent* OldRoot = GetRootComponent();
	Body->RegisterComponent();
	SetRootComponent(Body);
	if (OldRoot)
	{
		OldRoot->DestroyComponent();
	}
	SetActorTransform(Start);

	Take37Visuals::Build(this, Body, Visuals, Kind, Size * 100.0, Color);

	ChainProp = NewObject<UChainPropComponent>(this, TEXT("ChainProp"));
	ChainProp->Category = EChainCategory::Effect;
	ChainProp->DisplayName = InName;
	ChainProp->BaseValue = 50.f;
	ChainProp->bListenForHits = false;
	ChainProp->RegisterComponent();
}

void ACueDeviceActor::SetHighlight(bool bOn)
{
	Take37Visuals::Tint(Visuals, nullptr, bOn ? 0.5f : 0.f);
}

void ACueDeviceActor::ResetCue()
{
	bFired = false;
	if (ChainProp)
	{
		ChainProp->ResetRuntime();
	}
}

void ACueDeviceActor::Fire()
{
	UWorld* World = GetWorld();
	UChainReactionSubsystem* Chain = World ? World->GetSubsystem<UChainReactionSubsystem>() : nullptr;
	if (bFired || !Chain || !ChainProp)
	{
		return;
	}
	bFired = true;
	Chain->AddEvent(ETakeEventType::Cue, FString::Printf(TEXT("CUE: %s"), *DisplayName));
	UE_LOG(LogTake37, Log, TEXT("Cue fired: %s"), *DisplayName);

	switch (CueType)
	{
	case ECueType::Sandbag:
	case ECueType::Chandelier:
		if (Payload && Payload->ChainProp)
		{
			Payload->SetPhysicsActive(true);
			Chain->StartChain(Payload->ChainProp, DisplayName);
		}
		break;

	case ECueType::Pyro:
	case ECueType::Wind:
	{
		Chain->StartChain(ChainProp, DisplayName);
		const FVector Origin = GetActorLocation();
		const FVector Fwd = GetActorForwardVector();
		for (const TWeakObjectPtr<UChainPropComponent>& P : Chain->GetProps())
		{
			UChainPropComponent* Prop = P.Get();
			if (!Prop || Prop == ChainProp || !Prop->GetOwner())
			{
				continue;
			}
			UPrimitiveComponent* Prim = Prop->GetBoundPrimitive();
			if (!Prim || !Prim->IsSimulatingPhysics())
			{
				continue;
			}
			const FVector To = Prim->GetComponentLocation() - Origin;
			if (CueType == ECueType::Pyro)
			{
				if (To.Size() > Radius)
				{
					continue;
				}
				Prim->AddRadialImpulse(Origin, Radius, Strength, ERadialImpulseFalloff::RIF_Linear, false);
				Chain->CreditLink(ChainProp, Prop, Strength, Prim->GetComponentLocation(), EChainLinkType::Cue);
			}
			else
			{
				// Wind: a long box in front of the fan; only light things move.
				const float Along = FVector::DotProduct(To, Fwd);
				const float Lateral = FMath::Abs(FVector::DotProduct(To, GetActorRightVector()));
				if (Along < 0.f || Along > 1500.f || Lateral > 500.f || Prim->GetMass() > 40.f)
				{
					continue;
				}
				Prim->AddImpulse(Fwd * Strength * FMath::Max(Prim->GetMass(), 1.f) * 0.1f);
				Chain->CreditLink(ChainProp, Prop, Strength, Prim->GetComponentLocation(), EChainLinkType::Trigger);
			}
		}
		break;
	}
	}
}
