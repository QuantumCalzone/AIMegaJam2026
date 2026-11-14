#include "Chain/PropVisuals.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Actor.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"

namespace
{
	UMaterialInterface* GetBaseMaterial()
	{
		static TWeakObjectPtr<UMaterialInterface> Cached;
		if (!Cached.IsValid())
		{
			UMaterialInterface* M = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Materials/M_Greybox.M_Greybox"));
			if (!M)
			{
				M = LoadObject<UMaterialInterface>(nullptr, TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
			}
			Cached = M;
		}
		return Cached.Get();
	}

	UStaticMesh* LoadShapeMesh(const TCHAR* Shape)
	{
		return LoadObject<UStaticMesh>(nullptr, *FString::Printf(TEXT("/Engine/BasicShapes/%s.%s"), Shape, Shape));
	}

	FLinearColor Mul(const FLinearColor& C, float F)
	{
		return FLinearColor(C.R * F, C.G * F, C.B * F, 1.f);
	}
}

namespace Take37Visuals
{
	UStaticMeshComponent* AddMesh(AActor* Owner, USceneComponent* Parent, const TCHAR* Shape, const FVector& Offset, const FVector& DimsCm, const FRotator& Rot, FName Socket)
	{
		UStaticMeshComponent* C = NewObject<UStaticMeshComponent>(Owner);
		C->SetMobility(EComponentMobility::Movable);
		C->SetStaticMesh(LoadShapeMesh(Shape));
		C->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		C->SetGenerateOverlapEvents(false);
		C->SetupAttachment(Parent, Socket);
		C->SetRelativeLocation(Offset);
		C->SetRelativeRotation(Rot);
		C->SetRelativeScale3D(DimsCm / 100.0);
		C->RegisterComponent();
		return C;
	}

	UStaticMeshComponent* Add(AActor* Owner, USceneComponent* Parent, TArray<FVisualPart>& Parts, const TCHAR* Shape,
		const FVector& Offset, const FVector& DimsCm, const FLinearColor& Color, const FRotator& Rot,
		float Emissive, float Roughness, float Metallic, FName Socket)
	{
		UStaticMeshComponent* C = AddMesh(Owner, Parent, Shape, Offset, DimsCm, Rot, Socket);
		FVisualPart Part;
		Part.Comp = C;
		Part.Base = Color;
		Part.Emissive = Emissive;
		if (UMaterialInterface* Base = GetBaseMaterial())
		{
			Part.MID = UMaterialInstanceDynamic::Create(Base, Owner);
			Part.MID->SetVectorParameterValue(TEXT("Color"), Color);
			Part.MID->SetScalarParameterValue(TEXT("Emissive"), Emissive);
			Part.MID->SetScalarParameterValue(TEXT("Roughness"), Roughness);
			Part.MID->SetScalarParameterValue(TEXT("Metallic"), Metallic);
			C->SetMaterial(0, Part.MID);
		}
		Parts.Add(Part);
		return C;
	}

	void Tint(TArray<FVisualPart>& Parts, const FLinearColor* Override, float Highlight)
	{
		for (FVisualPart& P : Parts)
		{
			if (!P.MID)
			{
				continue;
			}
			FLinearColor C = Override ? *Override : P.Base;
			C = FMath::Lerp(C, FLinearColor::White, Highlight);
			P.MID->SetVectorParameterValue(TEXT("Color"), C);
			// Ghost previews and highlights glow so they read against the set.
			P.MID->SetScalarParameterValue(TEXT("Emissive"), (Override || Highlight > 0.f) ? FMath::Max(P.Emissive, 0.35f) : P.Emissive);
		}
	}

	void Build(AActor* O, USceneComponent* R, TArray<FVisualPart>& P, const FString& Kind, const FVector& Size, const FLinearColor& Color)
	{
		auto B = [&](FVector Off, FVector D, FLinearColor C, FRotator Rot = FRotator::ZeroRotator, float Em = 0.f, float Rough = 0.55f, float Met = 0.f)
		{
			return Add(O, R, P, TEXT("Cube"), Off, D, C, Rot, Em, Rough, Met);
		};
		auto Cy = [&](FVector Off, FVector D, FLinearColor C, FRotator Rot = FRotator::ZeroRotator, float Em = 0.f, float Rough = 0.55f, float Met = 0.f)
		{
			return Add(O, R, P, TEXT("Cylinder"), Off, D, C, Rot, Em, Rough, Met);
		};
		auto Sp = [&](FVector Off, FVector D, FLinearColor C, float Em = 0.f, float Rough = 0.45f)
		{
			return Add(O, R, P, TEXT("Sphere"), Off, D, C, FRotator::ZeroRotator, Em, Rough, 0.f);
		};
		const float W = Size.X, D = Size.Y, H = Size.Z;
		const float HH = H * 0.5f;
		const FLinearColor Steel(0.45f, 0.48f, 0.55f);
		const FLinearColor Black(0.03f, 0.03f, 0.04f);
		const FLinearColor Brass(0.95f, 0.7f, 0.2f);
		const FLinearColor Wood(0.5f, 0.28f, 0.12f);
		const FLinearColor White(0.95f, 0.95f, 0.92f);
		const FRotator AlongX(0.f, 0.f, 90.f);   // cylinder axis along Y
		const FRotator AxisX(90.f, 0.f, 0.f);    // cylinder axis along X

		if (Kind == TEXT("Chair"))
		{
			B(FVector(0, 0, -HH * 0.05f), FVector(W, D, 6), Color);
			for (int32 sx : { -1, 1 })
			{
				for (int32 sy : { -1, 1 })
				{
					B(FVector(sx * W * 0.4f, sy * D * 0.4f, -HH * 0.55f), FVector(6, 6, H * 0.5f), Mul(Color, 0.6f));
				}
			}
			B(FVector(0, D * 0.45f, HH * 0.45f), FVector(W, 5, H * 0.55f), Mul(Color, 0.75f));
			for (int32 i = -1; i <= 1; ++i)
			{
				B(FVector(i * W * 0.3f, D * 0.42f, HH * 0.45f), FVector(5, 3, H * 0.5f), Brass, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
			}
		}
		else if (Kind == TEXT("Table"))
		{
			B(FVector(0, 0, HH - 4), FVector(W, D, 8), Color);
			B(FVector(0, 0, HH - 8), FVector(W * 0.92f, D * 0.92f, 4), Mul(Color, 0.6f));
			for (int32 sx : { -1, 1 })
			{
				for (int32 sy : { -1, 1 })
				{
					B(FVector(sx * W * 0.42f, sy * D * 0.42f, -4), FVector(9, 9, H - 10), Mul(Color, 0.7f));
				}
			}
			// Red checkered cloth strip
			B(FVector(0, 0, HH + 0.5f), FVector(W * 0.5f, D * 1.02f, 1.5f), FLinearColor(0.8f, 0.1f, 0.1f));
		}
		else if (Kind == TEXT("Barrel"))
		{
			Cy(FVector(0, 0, 0), FVector(W, D, H), Color, FRotator::ZeroRotator, 0.f, 0.7f);
			Sp(FVector(0, 0, 0), FVector(W * 1.12f, D * 1.12f, H * 0.55f), Color);
			for (float z : { -0.32f, 0.f, 0.32f })
			{
				Cy(FVector(0, 0, z * H), FVector(W * 1.1f, D * 1.1f, 5), FLinearColor(0.15f, 0.15f, 0.17f), FRotator::ZeroRotator, 0.f, 0.35f, 0.9f);
			}
			Cy(FVector(0, 0, HH), FVector(W * 0.9f, D * 0.9f, 3), Mul(Color, 0.55f));
		}
		else if (Kind == TEXT("LightStand"))
		{
			Cy(FVector(0, 0, 0), FVector(7, 7, H), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
			for (int32 i = 0; i < 3; ++i)
			{
				const float A = FMath::DegreesToRadians(i * 120.f + 30.f);
				Cy(FVector(FMath::Cos(A) * 22, FMath::Sin(A) * 22, -HH + 6), FVector(5, 5, 50), Steel, FRotator(0, 0, 0), 0.f, 0.3f, 0.8f)
					->SetRelativeRotation(FRotator(FMath::Sin(A) * 60.f, 0.f, -FMath::Cos(A) * 60.f));
			}
			B(FVector(0, -8, HH - 14), FVector(46, 30, 36), Black, FRotator(25, 0, 0));
			B(FVector(0, -24, HH - 18), FVector(40, 3, 30), FLinearColor(1.f, 0.9f, 0.5f), FRotator(25, 0, 0), 4.f);
			B(FVector(0, -2, HH - 14), FVector(52, 3, 42), Black, FRotator(25, 0, 0));
		}
		else if (Kind == TEXT("HeroCamera"))
		{
			B(FVector(0, 0, 0), FVector(W * 0.8f, D * 0.8f, H * 0.8f), FLinearColor(0.07f, 0.07f, 0.09f), FRotator::ZeroRotator, 0.f, 0.3f, 0.4f);
			Cy(FVector(0, -D * 0.55f, 4), FVector(30, 30, 42), Steel, AlongX, 0.f, 0.2f, 0.9f);
			Cy(FVector(0, -D * 0.78f, 4), FVector(40, 40, 18), Black, AlongX);
			Sp(FVector(0, -D * 0.84f, 4), FVector(26, 6, 26), FLinearColor(0.1f, 0.3f, 0.6f), 0.6f, 0.05f);
			B(FVector(0, D * 0.25f, HH + 14), FVector(W * 0.75f, D * 0.55f, 26), FLinearColor(0.12f, 0.12f, 0.15f));
			Cy(FVector(0, D * 0.1f, HH + 28), FVector(34, 34, 8), Steel, AlongX, 0.f, 0.3f, 0.8f);
			Sp(FVector(W * 0.3f, -D * 0.35f, HH - 4), FVector(10, 10, 10), FLinearColor(1.f, 0.05f, 0.05f), 8.f);
			// Gold trim so the $2M camera is unmistakable
			B(FVector(0, 0, HH * 0.7f), FVector(W * 0.84f, D * 0.84f, 5), Brass, FRotator::ZeroRotator, 1.5f, 0.2f, 1.f);
			B(FVector(0, 0, -HH * 0.7f), FVector(W * 0.84f, D * 0.84f, 5), Brass, FRotator::ZeroRotator, 1.5f, 0.2f, 1.f);
		}
		else if (Kind == TEXT("Piano"))
		{
			B(FVector(0, 0, -6), FVector(W, D, H * 0.85f), FLinearColor(0.05f, 0.04f, 0.04f), FRotator::ZeroRotator, 0.f, 0.15f);
			B(FVector(0, 0, HH - 6), FVector(W * 1.02f, D * 1.02f, 8), FLinearColor(0.08f, 0.06f, 0.06f), FRotator::ZeroRotator, 0.f, 0.15f);
			B(FVector(0, -D * 0.6f, 4), FVector(W * 0.95f, 22, 8), White);
			for (int32 i = -6; i <= 6; ++i)
			{
				B(FVector(i * W * 0.07f, -D * 0.6f, 9), FVector(4, 14, 4), Black);
			}
			B(FVector(0, D * 0.2f, HH + 12), FVector(W * 0.92f, 6, 40), Wood);
			for (int32 sx : { -1, 1 })
			{
				B(FVector(sx * W * 0.45f, -D * 0.1f, -HH + 6), FVector(10, D * 0.8f, 14), Mul(Wood, 0.6f));
			}
		}
		else if (Kind == TEXT("Door"))
		{
			B(FVector(0, 0, 0), FVector(W, D, H), Color);
			for (float z : { -0.3f, 0.3f })
			{
				B(FVector(0, 0, z * H), FVector(W * 0.8f, D * 2.5f, 8), Mul(Color, 0.6f));
			}
			B(FVector(0, 0, HH - 12), FVector(W, D * 1.5f, 10), Brass, FRotator::ZeroRotator, 0.f, 0.3f, 0.9f);
		}
		else if (Kind == TEXT("Ladder"))
		{
			for (int32 sx : { -1, 1 })
			{
				B(FVector(sx * W * 0.42f, 0, 0), FVector(6, D, H), Color);
			}
			for (int32 i = 0; i < 8; ++i)
			{
				B(FVector(0, 0, -HH + 20 + i * ((H - 40) / 7.f)), FVector(W * 0.85f, D * 0.9f, 5), Mul(Color, 0.75f));
			}
		}
		else if (Kind == TEXT("PaintCan"))
		{
			Cy(FVector(0, 0, 0), FVector(W, D, H), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
			Cy(FVector(0, 0, HH * 0.1f), FVector(W * 1.02f, D * 1.02f, H * 0.5f), Color, FRotator::ZeroRotator, 0.2f);
			Cy(FVector(0, 0, HH), FVector(W * 1.05f, D * 1.05f, 2.5f), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
			Cy(FVector(0, 0, HH + 1.5f), FVector(W * 0.8f, D * 0.8f, 1.5f), Color, FRotator::ZeroRotator, 0.5f);
		}
		else if (Kind == TEXT("Rack"))
		{
			for (int32 sx : { -1, 1 })
			{
				B(FVector(sx * W * 0.46f, 0, 0), FVector(5, 5, H), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
				B(FVector(sx * W * 0.46f, 0, -HH + 3), FVector(8, D, 6), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.8f);
			}
			Cy(FVector(0, 0, HH - 12), FVector(5, 5, W * 0.92f), Steel, AxisX, 0.f, 0.3f, 0.8f);
			const FLinearColor Garments[] = { FLinearColor(0.8f, 0.1f, 0.2f), FLinearColor(0.1f, 0.4f, 0.8f), FLinearColor(0.95f, 0.75f, 0.1f), FLinearColor(0.5f, 0.15f, 0.6f), FLinearColor(0.1f, 0.6f, 0.35f), FLinearColor(0.95f, 0.45f, 0.1f) };
			for (int32 i = 0; i < 6; ++i)
			{
				B(FVector(-W * 0.38f + i * W * 0.15f, 0, HH - 70), FVector(W * 0.12f, 14, 110), Garments[i], FRotator::ZeroRotator, 0.f, 0.9f);
			}
		}
		else if (Kind == TEXT("Urn"))
		{
			Cy(FVector(0, 0, -2), FVector(W, D, H * 0.85f), Steel, FRotator::ZeroRotator, 0.f, 0.2f, 0.9f);
			Sp(FVector(0, 0, HH - 6), FVector(W * 0.9f, D * 0.9f, 14), Steel, 0.f, 0.2f);
			B(FVector(W * 0.5f, 0, -4), FVector(8, 6, 8), Black);
			B(FVector(0, 0, 4), FVector(W * 1.02f, D * 1.02f, 3), Black);
		}
		else if (Kind == TEXT("Cooler"))
		{
			B(FVector(0, 0, -H * 0.2f), FVector(W, D, H * 0.6f), White, FRotator::ZeroRotator, 0.f, 0.4f);
			Cy(FVector(0, 0, HH * 0.55f), FVector(W * 0.8f, D * 0.8f, H * 0.4f), FLinearColor(0.35f, 0.7f, 1.f), FRotator::ZeroRotator, 0.5f, 0.05f);
			B(FVector(0, -D * 0.5f, -H * 0.1f), FVector(10, 4, 8), FLinearColor(0.1f, 0.4f, 1.f));
			B(FVector(0, -D * 0.5f, -H * 0.25f), FVector(10, 4, 8), FLinearColor(1.f, 0.2f, 0.2f));
		}
		else if (Kind == TEXT("CakeTier") || Kind == TEXT("CakeTop"))
		{
			Cy(FVector(0, 0, 0), FVector(W, D, H), Color, FRotator::ZeroRotator, 0.15f, 0.8f);
			Cy(FVector(0, 0, HH), FVector(W * 1.04f, D * 1.04f, 4), White, FRotator::ZeroRotator, 0.15f, 0.6f);
			for (int32 i = 0; i < 10; ++i)
			{
				const float A = i * 36.f * PI / 180.f;
				Sp(FVector(FMath::Cos(A) * W * 0.5f, FMath::Sin(A) * D * 0.5f, HH - 2), FVector(7, 7, 7), White, 0.1f);
			}
			if (Kind == TEXT("CakeTop"))
			{
				Sp(FVector(0, 0, HH + 8), FVector(14, 14, 14), FLinearColor(1.f, 0.05f, 0.1f), 1.5f, 0.1f);
			}
		}
		else if (Kind == TEXT("Cactus"))
		{
			Cy(FVector(0, 0, 0), FVector(W * 0.5f, D * 0.5f, H), Color, FRotator::ZeroRotator, 0.f, 0.8f);
			Sp(FVector(0, 0, HH), FVector(W * 0.5f, D * 0.5f, W * 0.5f), Color, 0.f, 0.8f);
			Cy(FVector(W * 0.38f, 0, 0), FVector(W * 0.25f, D * 0.25f, W * 0.6f), Color, AxisX, 0.f, 0.8f);
			Cy(FVector(W * 0.62f, 0, H * 0.2f), FVector(W * 0.25f, D * 0.25f, H * 0.4f), Color, FRotator::ZeroRotator, 0.f, 0.8f);
			Cy(FVector(0, 0, -HH + 5), FVector(W * 0.9f, D * 0.9f, 10), FLinearColor(0.6f, 0.3f, 0.15f));
			Sp(FVector(0, -2, HH + 4), FVector(7, 7, 7), FLinearColor(1.f, 0.4f, 0.6f), 0.6f);
		}
		else if (Kind == TEXT("HatBox"))
		{
			Cy(FVector(0, 0, 0), FVector(W, D, H), Color, FRotator::ZeroRotator, 0.f, 0.8f);
			Cy(FVector(0, 0, HH - 4), FVector(W * 1.08f, D * 1.08f, 8), Mul(Color, 0.8f));
			Cy(FVector(0, 0, 0), FVector(W * 1.02f, D * 1.02f, 6), FLinearColor(0.85f, 0.1f, 0.15f));
		}
		else if (Kind == TEXT("Sandbag"))
		{
			Sp(FVector(0, 0, -2), FVector(W, D, H * 1.1f), Color, 0.f, 0.95f);
			Sp(FVector(0, 0, HH + 2), FVector(W * 0.3f, D * 0.5f, 10), Mul(Color, 0.7f), 0.f, 0.9f);
			Cy(FVector(0, 0, HH + 24), FVector(3, 3, 44), FLinearColor(0.55f, 0.4f, 0.2f), FRotator::ZeroRotator, 0.f, 0.95f);
			B(FVector(0, 0, 4), FVector(W * 0.2f, D * 1.02f, H * 0.2f), FLinearColor(0.85f, 0.15f, 0.1f), FRotator::ZeroRotator, 0.f, 0.9f);
		}
		else if (Kind == TEXT("Chandelier"))
		{
			Cy(FVector(0, 0, 0), FVector(W, D, 6), Brass, FRotator::ZeroRotator, 0.8f, 0.2f, 1.f);
			Cy(FVector(0, 0, 6), FVector(W * 0.6f, D * 0.6f, 6), Brass, FRotator::ZeroRotator, 0.8f, 0.2f, 1.f);
			for (int32 i = 0; i < 8; ++i)
			{
				const float A = i * 45.f * PI / 180.f;
				const FVector Pos(FMath::Cos(A) * W * 0.46f, FMath::Sin(A) * D * 0.46f, 0);
				Cy(Pos + FVector(0, 0, 14), FVector(5, 5, 22), White);
				Sp(Pos + FVector(0, 0, 30), FVector(8, 8, 12), FLinearColor(1.f, 0.85f, 0.4f), 12.f, 0.1f);
			}
			Sp(FVector(0, 0, 0), FVector(W * 0.22f, D * 0.22f, W * 0.22f), Brass, 0.8f, 0.2f);
			Cy(FVector(0, 0, 40), FVector(4, 4, 100), Brass, FRotator::ZeroRotator, 0.3f, 0.2f, 1.f);
		}
		else if (Kind == TEXT("Banana"))
		{
			Sp(FVector(0, 0, 0), FVector(W, D, H * 1.6f), FLinearColor(1.f, 0.88f, 0.05f), 0.6f, 0.3f);
			Sp(FVector(W * 0.45f, 0, 0), FVector(W * 0.2f, D * 0.5f, H * 1.4f), FLinearColor(0.3f, 0.2f, 0.05f), 0.f, 0.5f);
			Sp(FVector(-W * 0.45f, 0, 0), FVector(W * 0.2f, D * 0.5f, H * 1.4f), FLinearColor(0.3f, 0.2f, 0.05f), 0.f, 0.5f);
		}
		else if (Kind == TEXT("Bowling"))
		{
			Sp(FVector(0, 0, 0), FVector(W, D, H), Color, 0.2f, 0.05f);
			Sp(FVector(W * 0.12f, -D * 0.25f, H * 0.4f), FVector(5, 5, 5), Black);
			Sp(FVector(-W * 0.05f, -D * 0.3f, H * 0.4f), FVector(5, 5, 5), Black);
			Sp(FVector(W * 0.02f, -D * 0.12f, H * 0.46f), FVector(5, 5, 5), Black);
			Sp(FVector(-W * 0.2f, D * 0.1f, H * 0.3f), FVector(W * 0.18f, D * 0.1f, H * 0.18f), FLinearColor(1.f, 1.f, 1.f), 0.8f, 0.1f);
		}
		else if (Kind == TEXT("Skateboard"))
		{
			B(FVector(0, 0, 2), FVector(W, D, 3), Color, FRotator::ZeroRotator, 0.3f, 0.4f);
			B(FVector(W * 0.5f, 0, 5), FVector(10, D, 3), Color, FRotator(0, 0, 0), 0.3f);
			B(FVector(-W * 0.5f, 0, 5), FVector(10, D, 3), Color, FRotator(0, 0, 0), 0.3f);
			B(FVector(0, 0, 3.6f), FVector(W * 0.9f, D * 0.8f, 0.6f), Black, FRotator::ZeroRotator, 0.f, 0.95f);
			for (int32 sx : { -1, 1 })
			{
				for (int32 sy : { -1, 1 })
				{
					Cy(FVector(sx * W * 0.34f, sy * D * 0.55f, -3), FVector(8, 8, 5), White, AlongX, 0.2f);
				}
				B(FVector(sx * W * 0.34f, 0, -1), FVector(5, D * 0.9f, 3), Steel, FRotator::ZeroRotator, 0.f, 0.3f, 0.9f);
			}
		}
		else if (Kind == TEXT("Cord"))
		{
			Cy(FVector(0, 0, 0), FVector(D, D, W * 0.92f), Color, AxisX, 0.4f, 0.6f);
			B(FVector(W * 0.5f - 6, 0, 0), FVector(12, D * 2.5f, D * 2.5f), Black);
			B(FVector(W * 0.5f + 2, 0, 0), FVector(4, 2, 5), Brass, FRotator::ZeroRotator, 0.f, 0.3f, 1.f);
			B(FVector(-W * 0.5f + 6, 0, 0), FVector(12, D * 2.5f, D * 2.5f), FLinearColor(0.9f, 0.85f, 0.2f));
		}
		else if (Kind == TEXT("BarCounter"))
		{
			B(FVector(0, 0, -4), FVector(W, D * 0.9f, H - 10), Mul(Color, 0.7f), FRotator::ZeroRotator, 0.f, 0.5f);
			for (int32 i = -4; i <= 4; ++i)
			{
				B(FVector(i * W * 0.1f, -D * 0.47f, -4), FVector(W * 0.085f, 3, H * 0.7f), Mul(Color, 0.9f));
			}
			B(FVector(0, 0, HH - 4), FVector(W * 1.02f, D * 1.15f, 9), Color, FRotator::ZeroRotator, 0.f, 0.15f);
			Cy(FVector(0, -D * 0.45f, -HH + 24), FVector(5, 5, W * 0.96f), Brass, AxisX, 0.4f, 0.2f, 1.f);
			for (int32 i = 0; i < 5; ++i)
			{
				Cy(FVector(-W * 0.35f + i * W * 0.17f, 0, HH + 12), FVector(8, 8, 24), FLinearColor(0.2f + 0.15f * i, 0.5f, 0.2f), FRotator::ZeroRotator, 0.4f, 0.05f);
			}
		}
		else if (Kind == TEXT("Winch"))
		{
			Cy(FVector(0, 0, 0), FVector(W * 0.9f, D * 0.9f, H), Steel, AxisX, 0.f, 0.3f, 0.8f);
			B(FVector(0, 0, HH), FVector(W * 1.4f, D * 1.2f, 6), Black);
			Cy(FVector(0, -D * 0.5f, 0), FVector(W * 1.1f, W * 1.1f, 4), FLinearColor(1.f, 0.8f, 0.1f), AlongX, 0.8f);
		}
		else if (Kind == TEXT("Pyro"))
		{
			B(FVector(0, 0, 0), FVector(W, D, H), FLinearColor(0.75f, 0.1f, 0.08f), FRotator::ZeroRotator, 0.2f, 0.7f);
			for (int32 i = -2; i <= 2; ++i)
			{
				B(FVector(i * W * 0.2f, -D * 0.5f - 0.5f, 0), FVector(W * 0.1f, 1.5f, H * 0.95f), FLinearColor(1.f, 0.85f, 0.1f), FRotator(0, 0, 0), 0.5f);
			}
			Cy(FVector(0, 0, HH + 8), FVector(10, 10, 16), Black);
			Sp(FVector(0, 0, HH + 20), FVector(12, 12, 12), FLinearColor(1.f, 0.4f, 0.05f), 10.f);
		}
		else if (Kind == TEXT("Fan"))
		{
			// Housing ring faces local +X; width is thin, so the disc spans Y/Z.
			Cy(FVector(0, 0, 0), FVector(D * 0.95f, H * 0.95f, W * 1.6f), Steel, AxisX, 0.f, 0.3f, 0.8f);
			Cy(FVector(0, 0, 0), FVector(D * 0.8f, H * 0.8f, W * 0.7f), FLinearColor(0.35f, 0.8f, 0.9f), AxisX, 0.4f, 0.2f);
			for (int32 i = 0; i < 3; ++i)
			{
				B(FVector(W * 0.3f, 0, 0), FVector(3, D * 0.7f, 8), White, FRotator(0, 0, i * 60.f), 0.2f);
			}
			Sp(FVector(W * 0.5f, 0, 0), FVector(14, 14, 14), Black);
			B(FVector(0, 0, -HH - 6), FVector(W * 3.f, D * 0.5f, 10), Black);
		}
		else
		{
			// Plain single-shape fallback
			const TCHAR* Shape = (Kind == TEXT("Sphere")) ? TEXT("Sphere") : (Kind == TEXT("Cylinder")) ? TEXT("Cylinder") : (Kind == TEXT("Cone")) ? TEXT("Cone") : TEXT("Cube");
			Add(O, R, P, Shape, FVector::ZeroVector, Size, Color);
		}
	}
}
