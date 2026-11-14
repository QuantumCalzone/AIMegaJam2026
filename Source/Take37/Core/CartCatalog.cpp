#include "Core/CartCatalog.h"

namespace Take37Cart
{
	const FCartItemInfo& Get(ECartItem Item)
	{
		static TMap<ECartItem, FCartItemInfo> Table;
		static FCartItemInfo Empty;
		if (Table.Num() == 0)
		{
			{
				FCartItemInfo I;
				I.Name = TEXT("Banana Peel");
				I.Cost = 50;
				I.Shape = TEXT("Cube");
				I.Kind = TEXT("Banana");
				I.Scale = FVector(0.42, 0.22, 0.06);
				I.MassKg = 0.2f;
				I.Color = FLinearColor(1.f, 0.85f, 0.05f);
				I.Value = 100.f;
				I.MinImpulse = 60.f;
				Table.Add(ECartItem::BananaPeel, I);
			}
			{
				FCartItemInfo I;
				I.Name = TEXT("Bowling Ball");
				I.Cost = 150;
				I.Shape = TEXT("Sphere");
				I.Kind = TEXT("Bowling");
				I.Scale = FVector(0.3, 0.3, 0.3);
				I.MassKg = 7.f;
				I.Color = FLinearColor(0.12f, 0.05f, 0.25f);
				I.Value = 200.f;
				I.MinImpulse = 500.f;
				I.bCanOrigin = true;
				Table.Add(ECartItem::BowlingBall, I);
			}
			{
				FCartItemInfo I;
				I.Name = TEXT("Skateboard");
				I.Cost = 150;
				I.Shape = TEXT("Cube");
				I.Kind = TEXT("Skateboard");
				I.Scale = FVector(0.9, 0.24, 0.1);
				I.MassKg = 3.f;
				I.Color = FLinearColor(1.f, 0.4f, 0.05f);
				I.Value = 150.f;
				I.MinImpulse = 300.f;
				I.bCanOrigin = true;
				Table.Add(ECartItem::Skateboard, I);
			}
			{
				FCartItemInfo I;
				I.Name = TEXT("Extension Cord");
				I.Cost = 50;
				I.Shape = TEXT("Cube");
				I.Kind = TEXT("Cord");
				I.Scale = FVector(1.6, 0.05, 0.05);
				I.MassKg = 0.5f;
				I.Color = FLinearColor(1.f, 0.55f, 0.05f);
				I.Value = 75.f;
				I.MinImpulse = 100.f;
				Table.Add(ECartItem::ExtensionCord, I);
			}
		}
		const FCartItemInfo* Found = Table.Find(Item);
		return Found ? *Found : Empty;
	}
}
