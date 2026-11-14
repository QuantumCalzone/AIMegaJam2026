#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Components/PrimitiveComponent.h"
#include "GameFramework/Actor.h"
#include "Engine/World.h"
#include "Take37.h"

UChainPropComponent::UChainPropComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

FString UChainPropComponent::GetLabel() const
{
	if (!DisplayName.IsEmpty())
	{
		return DisplayName;
	}
	return GetOwner() ? GetOwner()->GetName() : TEXT("Prop");
}

void UChainPropComponent::ResetRuntime()
{
	ChainId = INDEX_NONE;
	ChainDepth = 0;
	LastInstigator.Reset();
	LastCreditTime = -1000.0;
	bImprov = false;
}

void UChainPropComponent::BeginPlay()
{
	Super::BeginPlay();

	if (bListenForHits && GetOwner())
	{
		if (UPrimitiveComponent* Prim = Cast<UPrimitiveComponent>(GetOwner()->GetRootComponent()))
		{
			Prim->SetNotifyRigidBodyCollision(true);
			Prim->OnComponentHit.AddUniqueDynamic(this, &UChainPropComponent::OnOwnerHit);
			BoundPrim = Prim;
		}
		else
		{
			UE_LOG(LogTake37, Warning, TEXT("ChainProp on %s has no root primitive; hits will not be tracked."), *GetOwner()->GetName());
		}
	}
	else if (GetOwner())
	{
		BoundPrim = Cast<UPrimitiveComponent>(GetOwner()->GetRootComponent());
	}

	if (UChainReactionSubsystem* Sub = GetWorld()->GetSubsystem<UChainReactionSubsystem>())
	{
		Sub->RegisterProp(this);
	}
}

void UChainPropComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (UPrimitiveComponent* Prim = BoundPrim.Get())
	{
		Prim->OnComponentHit.RemoveDynamic(this, &UChainPropComponent::OnOwnerHit);
	}
	if (UWorld* World = GetWorld())
	{
		if (UChainReactionSubsystem* Sub = World->GetSubsystem<UChainReactionSubsystem>())
		{
			Sub->UnregisterProp(this);
		}
	}
	Super::EndPlay(EndPlayReason);
}

void UChainPropComponent::OnOwnerHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
	if (!OtherActor)
	{
		return;
	}
	UChainPropComponent* Other = OtherActor->FindComponentByClass<UChainPropComponent>();
	if (!Other || Other == this)
	{
		return;
	}
	if (UChainReactionSubsystem* Sub = GetWorld()->GetSubsystem<UChainReactionSubsystem>())
	{
		Sub->ReportHit(this, Other, NormalImpulse.Size(), Hit.ImpactPoint);
	}
}
