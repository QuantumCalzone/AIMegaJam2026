#pragma once

#include "CoreMinimal.h"

class AActor;
class USceneComponent;
class UStaticMeshComponent;
class UMaterialInstanceDynamic;

/** One rendered piece of a composite prop. */
struct FVisualPart
{
	UStaticMeshComponent* Comp = nullptr;
	UMaterialInstanceDynamic* MID = nullptr;
	FLinearColor Base = FLinearColor::White;
	float Emissive = 0.f;
};

/**
 * Procedural stylised models built from engine basic shapes. Collision lives on a separate shape component,
 * so these parts are visual only and may be rotated freely.
 */
namespace Take37Visuals
{
	UStaticMeshComponent* Add(AActor* Owner, USceneComponent* Parent, TArray<FVisualPart>& Parts, const TCHAR* Shape,
		const FVector& Offset, const FVector& DimsCm, const FLinearColor& Color, const FRotator& Rot = FRotator::ZeroRotator,
		float Emissive = 0.f, float Roughness = 0.55f, float Metallic = 0.f, FName Socket = NAME_None);

	/** Builds the model for Kind. SizeCm is the full size of the collision shape; Color is the prop's main colour. */
	void Build(AActor* Owner, USceneComponent* Parent, TArray<FVisualPart>& Parts, const FString& Kind, const FVector& SizeCm, const FLinearColor& Color);

	/** Colour every part with Override, or restore base colours when Override is null. Highlight lerps to white. */
	void Tint(TArray<FVisualPart>& Parts, const FLinearColor* Override, float Highlight);

	UStaticMeshComponent* AddMesh(AActor* Owner, USceneComponent* Parent, const TCHAR* Shape, const FVector& Offset, const FVector& DimsCm, const FRotator& Rot, FName Socket = NAME_None);
}
