#include "Core/Take37Stage.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Core/TakeDirectorSubsystem.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/PointLight.h"
#include "Engine/PostProcessVolume.h"
#include "Engine/SkyLight.h"
#include "Engine/World.h"
#include "Take37.h"

ATake37Stage::ATake37Stage()
{
	PrimaryActorTick.bCanEverTick = false;
	SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("Root")));
}

void ATake37Stage::BeginPlay()
{
	Super::BeginPlay();

	BuildLighting();
	BuildStage();
	BuildCast();

	if (UTakeDirectorSubsystem* Director = GetWorld()->GetSubsystem<UTakeDirectorSubsystem>())
	{
		Director->RegisterStage(this);
		Director->OnPhaseChanged.AddUObject(this, &ATake37Stage::HandlePhaseChanged);

		// Default cue slots: sandbag, pyro, wind. The player can reassign in Setup.
		int32 Slot = 0;
		for (ECueType Wanted : { ECueType::Sandbag, ECueType::Pyro, ECueType::Wind })
		{
			for (ACueDeviceActor* D : Devices)
			{
				if (D && D->CueType == Wanted)
				{
					Director->AssignCue(Slot++, D);
					break;
				}
			}
		}
		Director->StartSetup();
	}
	UE_LOG(LogTake37, Log, TEXT("Stage built: %d props, %d cue devices"), Props.Num(), Devices.Num());
}

void ATake37Stage::RegisterProp(ATake37PropActor* Prop)
{
	if (Prop)
	{
		Props.AddUnique(Prop);
	}
}

void ATake37Stage::UnregisterProp(ATake37PropActor* Prop)
{
	Props.Remove(Prop);
}

void ATake37Stage::HandlePhaseChanged(ETake37Phase Old, ETake37Phase New)
{
	if (New == ETake37Phase::Take)
	{
		for (AStageActorCharacter* A : Actors)
		{
			if (A)
			{
				A->StartRoute();
			}
		}
		for (ATake37PropActor* P : Props)
		{
			if (P && P->Spec.bSimulateInTake)
			{
				P->SetPhysicsActive(true);
			}
		}
	}
	else if (New == ETake37Phase::Setup)
	{
		ResetAll();
	}
}

void ATake37Stage::ResetAll()
{
	for (AStageActorCharacter* A : Actors)
	{
		if (A)
		{
			A->ResetToStart();
		}
	}
	for (ATake37PropActor* P : Props)
	{
		if (P)
		{
			P->ResetToHome();
		}
	}
	for (ACueDeviceActor* D : Devices)
	{
		if (D)
		{
			D->ResetCue();
		}
	}
}

ATake37PropActor* ATake37Stage::SpawnProp(const FPropSpec& Spec, const FVector& BottomLocation, const FRotator& Rotation, bool bLocationIsCenter)
{
	FVector Location = BottomLocation;
	if (!bLocationIsCenter)
	{
		Location.Z += Spec.Scale.Z * 50.0;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	ATake37PropActor* Prop = GetWorld()->SpawnActor<ATake37PropActor>(Location, Rotation, Params);
	if (Prop)
	{
		Prop->Configure(Spec);
		Props.Add(Prop);
	}
	return Prop;
}

ACueDeviceActor* ATake37Stage::SpawnDevice(ECueType Type, const FString& Name, const FVector& BottomLocation, const FVector& Size, const FLinearColor& Color, const FString& Kind, float Yaw)
{
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	ACueDeviceActor* Device = GetWorld()->SpawnActor<ACueDeviceActor>(BottomLocation + FVector(0, 0, Size.Z * 50.0), FRotator(0, Yaw, 0), Params);
	if (Device)
	{
		Device->Setup(Type, Name, Size, Color, Kind);
		Devices.Add(Device);
	}
	return Device;
}

void ATake37Stage::AddSign(const FString& Text, const FVector& Location, float WorldSize, const FColor& Color)
{
	UTextRenderComponent* T = NewObject<UTextRenderComponent>(this);
	T->SetMobility(EComponentMobility::Movable);
	T->SetText(FText::FromString(Text));
	T->SetWorldSize(WorldSize);
	T->SetTextRenderColor(Color);
	T->SetHorizontalAlignment(EHTA_Center);
	T->SetVerticalAlignment(EVRTA_TextCenter);
	T->SetupAttachment(GetRootComponent());
	T->SetRelativeLocation(Location);
	T->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));   // faces the audience (-Y)
	T->RegisterComponent();
}

void ATake37Stage::BuildLighting()
{
	UWorld* World = GetWorld();

	// Warm key light from front-left, cool fill from the opposite side. Both cast no static light.
	{
		const FTransform T(FRotator(-52.f, -28.f, 0.f));
		if (ADirectionalLight* Key = World->SpawnActorDeferred<ADirectionalLight>(ADirectionalLight::StaticClass(), T))
		{
			Key->GetLightComponent()->SetMobility(EComponentMobility::Movable);
			Key->GetLightComponent()->SetIntensity(11.f);
			Key->GetLightComponent()->SetLightColor(FLinearColor(1.f, 0.93f, 0.8f));
			Key->FinishSpawning(T);
		}
	}
	{
		const FTransform T(FRotator(-35.f, 150.f, 0.f));
		if (ADirectionalLight* Fill = World->SpawnActorDeferred<ADirectionalLight>(ADirectionalLight::StaticClass(), T))
		{
			Fill->GetLightComponent()->SetMobility(EComponentMobility::Movable);
			Fill->GetLightComponent()->SetIntensity(3.f);
			Fill->GetLightComponent()->SetLightColor(FLinearColor(0.7f, 0.8f, 1.f));
			Fill->GetLightComponent()->SetCastShadows(false);
			Fill->FinishSpawning(T);
		}
	}
	if (ASkyLight* Sky = World->SpawnActorDeferred<ASkyLight>(ASkyLight::StaticClass(), FTransform::Identity))
	{
		Sky->GetLightComponent()->SetMobility(EComponentMobility::Movable);
		Sky->GetLightComponent()->bLowerHemisphereIsBlack = false;
		Sky->GetLightComponent()->SetIntensity(2.f);
		Sky->FinishSpawning(FTransform::Identity);
		Sky->GetLightComponent()->SetRealTimeCaptureEnabled(true);
	}

	// Warm practical lights over the set pieces so every zone reads.
	const TArray<TPair<FVector, FLinearColor>> Practicals = {
		{ FVector(-780, 300, 380), FLinearColor(1.f, 0.7f, 0.35f) },
		{ FVector(800, -350, 260), FLinearColor(1.f, 0.85f, 0.7f) },
		{ FVector(150, -150, 420), FLinearColor(1.f, 0.95f, 0.85f) },
		{ FVector(950, 560, 300), FLinearColor(1.f, 0.75f, 0.45f) },
	};
	for (const TPair<FVector, FLinearColor>& L : Practicals)
	{
		const FTransform T(L.Key);
		if (APointLight* P = World->SpawnActorDeferred<APointLight>(APointLight::StaticClass(), T))
		{
			P->GetLightComponent()->SetMobility(EComponentMobility::Movable);
			P->GetLightComponent()->SetIntensity(9000.f);
			Cast<UPointLightComponent>(P->GetLightComponent())->SetAttenuationRadius(900.f);
			P->GetLightComponent()->SetLightColor(L.Value);
			P->FinishSpawning(T);
		}
	}

	// Cinematic grade: richer colour, soft bloom, vignette, light grain, clamped exposure.
	if (APostProcessVolume* PP = World->SpawnActor<APostProcessVolume>(FVector::ZeroVector, FRotator::ZeroRotator))
	{
		PP->bUnbound = true;
		FPostProcessSettings& S = PP->Settings;
		S.bOverride_ColorSaturation = true;
		S.ColorSaturation = FVector4(1.18f, 1.18f, 1.18f, 1.f);
		S.bOverride_ColorContrast = true;
		S.ColorContrast = FVector4(1.08f, 1.08f, 1.08f, 1.f);
		S.bOverride_BloomIntensity = true;
		S.BloomIntensity = 0.6f;
		S.bOverride_VignetteIntensity = true;
		S.VignetteIntensity = 0.45f;
		S.bOverride_FilmGrainIntensity = true;
		S.FilmGrainIntensity = 0.12f;
		S.bOverride_AutoExposureBias = true;
		S.AutoExposureBias = 0.6f;
		S.bOverride_AutoExposureMinBrightness = true;
		S.AutoExposureMinBrightness = 0.8f;
		S.bOverride_AutoExposureMaxBrightness = true;
		S.AutoExposureMaxBrightness = 1.6f;
	}
}

void ATake37Stage::BuildStage()
{
	const FLinearColor Wood(0.45f, 0.24f, 0.1f);
	const FLinearColor Steel(0.45f, 0.48f, 0.55f);
	const FLinearColor Gold(1.f, 0.75f, 0.2f);
	const FLinearColor Chair(0.7f, 0.3f, 0.12f);

	// Static set piece with a custom model.
	auto Static = [this](const TCHAR* Name, const TCHAR* Kind, FVector Bottom, FVector DimsCm, FLinearColor Color, FRotator Rot = FRotator::ZeroRotator, bool bCenter = false)
	{
		FPropSpec S;
		S.Name = Name;
		S.Shape = TEXT("Cube");
		S.Kind = Kind;
		S.Scale = DimsCm / 100.0;
		S.Color = Color;
		return SpawnProp(S, Bottom, Rot, bCenter);
	};

	// Tracked physics prop. Dimensions in cm; Shape picks the collision primitive.
	auto Dyn = [this](const TCHAR* Name, const TCHAR* Kind, const TCHAR* Shape, FVector Bottom, FVector DimsCm, FLinearColor Color, float Mass, EChainCategory Cat, float Value, float MinImpulse = 1500.f)
	{
		FPropSpec S;
		S.Name = Name;
		S.Kind = Kind;
		S.Shape = Shape;
		S.Scale = DimsCm / 100.0;
		S.Color = Color;
		S.bDynamic = true;
		S.bTracked = true;
		S.MassKg = Mass;
		S.Category = Cat;
		S.Value = Value;
		S.MinImpulse = MinImpulse;
		return SpawnProp(S, Bottom);
	};

	// --- Floor, painted desert backdrop, curtains, rigging (all static) ---
	Static(TEXT("Stage Floor"), TEXT("Cube"), FVector(0, 0, -100), FVector(2600, 1800, 100), FLinearColor(0.42f, 0.27f, 0.15f));
	for (int32 i = -12; i <= 12; ++i)
	{
		Static(TEXT("Floor Plank Line"), TEXT("Cube"), FVector(i * 100, 0, 0.3), FVector(2.f, 1800, 0.6f), FLinearColor(0.2f, 0.12f, 0.06f));
	}
	Static(TEXT("Backdrop Sand"), TEXT("Cube"), FVector(0, 920, 0), FVector(2600, 20, 180), FLinearColor(0.9f, 0.68f, 0.38f));
	Static(TEXT("Backdrop Dusk"), TEXT("Cube"), FVector(0, 920, 180), FVector(2600, 20, 150), FLinearColor(1.f, 0.5f, 0.25f));
	Static(TEXT("Backdrop Sky"), TEXT("Cube"), FVector(0, 920, 330), FVector(2600, 20, 400), FLinearColor(0.25f, 0.5f, 0.95f));
	Static(TEXT("Mesa A"), TEXT("Cone"), FVector(-300, 890, 150), FVector(600, 30, 260), FLinearColor(0.65f, 0.3f, 0.2f));
	Static(TEXT("Mesa B"), TEXT("Cone"), FVector(500, 890, 150), FVector(800, 30, 200), FLinearColor(0.75f, 0.38f, 0.22f));
	Static(TEXT("Painted Sun"), TEXT("Sphere"), FVector(900, 895, 330), FVector(220, 20, 220), FLinearColor(1.f, 0.9f, 0.4f));
	for (int32 sx : { -1, 1 })
	{
		Static(TEXT("Curtain"), TEXT("Cube"), FVector(sx * 1330, 0, 0), FVector(50, 1800, 520), FLinearColor(0.6f, 0.05f, 0.1f));
		Static(TEXT("Curtain Trim"), TEXT("Cube"), FVector(sx * 1330, 0, 520), FVector(60, 1800, 28), Gold);
	}
	Static(TEXT("Truss"), TEXT("Cube"), FVector(0, 860, 540), FVector(2500, 14, 14), Steel);
	for (int32 i = -4; i <= 4; ++i)
	{
		Static(TEXT("Rig Lamp"), TEXT("Cube"), FVector(i * 270, 840, 500), FVector(40, 34, 36), FLinearColor(0.04f, 0.04f, 0.05f));
		FPropSpec Glow;
		Glow.Name = TEXT("Rig Lamp Lens");
		Glow.Kind = TEXT("Cube");
		Glow.Scale = FVector(0.3, 0.02, 0.28);
		Glow.Color = FLinearColor(1.f, 0.9f, 0.55f);
		SpawnProp(Glow, FVector(i * 270, 821, 504));
	}

	// Gaffer-tape X marks (blocking marks, GDD section 2.1)
	for (const FVector2D& M : { FVector2D(-260, -420), FVector2D(150, -520), FVector2D(560, -520), FVector2D(-700, 40) })
	{
		for (float Yaw : { 45.f, -45.f })
		{
			Static(TEXT("Tape Mark"), TEXT("Cube"), FVector(M.X, M.Y, 0.4), FVector(70, 7, 1.f), FLinearColor(0.2f, 1.f, 0.55f), FRotator(0, Yaw, 0));
		}
	}

	// --- Saloon set (left) ---
	Static(TEXT("Saloon Facade"), TEXT("Cube"), FVector(-850, 850, 0), FVector(900, 18, 440), FLinearColor(0.7f, 0.38f, 0.18f));
	Static(TEXT("Saloon Parapet"), TEXT("Cube"), FVector(-850, 846, 440), FVector(980, 22, 90), FLinearColor(0.55f, 0.15f, 0.1f));
	Static(TEXT("Facade Door Gap"), TEXT("Cube"), FVector(-850, 838, 0), FVector(190, 6, 240), FLinearColor(0.08f, 0.04f, 0.03f));
	for (int32 sx : { -1, 1 })
	{
		Static(TEXT("Facade Window"), TEXT("Cube"), FVector(-850 + sx * 300, 838, 130), FVector(140, 6, 150), FLinearColor(1.f, 0.78f, 0.35f));
	}
	AddSign(TEXT("SALOON"), FVector(-850, 830, 485), 70.f, FColor(255, 224, 120));
	AddSign(TEXT("SOUNDSTAGE 4  -  TAKE 37"), FVector(0, 880, 640), 55.f, FColor(255, 255, 255));

	Static(TEXT("Bar Counter"), TEXT("BarCounter"), FVector(-1000, 620, 0), FVector(420, 90, 115), FLinearColor(0.35f, 0.17f, 0.08f));
	Dyn(TEXT("Piano"), TEXT("Piano"), TEXT("Cube"), FVector(-1180, 330, 0), FVector(170, 80, 120), FLinearColor(0.05f, 0.04f, 0.04f), 120.f, EChainCategory::Furniture, 300.f, 3000.f);
	Dyn(TEXT("Swinging Door L"), TEXT("Door"), TEXT("Cube"), FVector(-910, 790, 0), FVector(95, 7, 190), Wood, 8.f, EChainCategory::Furniture, 100.f);
	Dyn(TEXT("Swinging Door R"), TEXT("Door"), TEXT("Cube"), FVector(-800, 790, 0), FVector(95, 7, 190), Wood, 8.f, EChainCategory::Furniture, 100.f);
	Dyn(TEXT("Saloon Table"), TEXT("Table"), TEXT("Cube"), FVector(-780, 300, 0), FVector(130, 130, 78), FLinearColor(0.5f, 0.28f, 0.12f), 20.f, EChainCategory::Furniture, 150.f);
	Dyn(TEXT("Chair A"), TEXT("Chair"), TEXT("Cube"), FVector(-950, 330, 0), FVector(48, 48, 95), Chair, 6.f, EChainCategory::Furniture, 100.f, 800.f)->Spec.bMovable = true;
	Dyn(TEXT("Chair B"), TEXT("Chair"), TEXT("Cube"), FVector(-620, 330, 0), FVector(48, 48, 95), Chair, 6.f, EChainCategory::Furniture, 100.f, 800.f)->Spec.bMovable = true;
	Dyn(TEXT("Chair C"), TEXT("Chair"), TEXT("Cube"), FVector(-780, 130, 0), FVector(48, 48, 95), Chair, 6.f, EChainCategory::Furniture, 100.f, 800.f)->Spec.bMovable = true;

	// --- Studio floor (centre) ---
	Static(TEXT("Dolly Rail A"), TEXT("Cube"), FVector(80, -150, 0), FVector(8, 520, 8), Steel);
	Static(TEXT("Dolly Rail B"), TEXT("Cube"), FVector(220, -150, 0), FVector(8, 520, 8), Steel);
	Static(TEXT("Dolly Base"), TEXT("Cube"), FVector(150, -150, 8), FVector(170, 190, 42), FLinearColor(0.12f, 0.12f, 0.16f));
	{
		FPropSpec S;
		S.Name = TEXT("$2M Hero Camera");
		S.Shape = TEXT("Cube");
		S.Kind = TEXT("HeroCamera");
		S.Scale = FVector(0.85, 1.05, 0.65);
		S.Color = FLinearColor(0.05f, 0.05f, 0.06f);
		S.bDynamic = true;
		S.bTracked = true;
		S.MassKg = 40.f;
		S.Category = EChainCategory::Camera;
		S.Value = 1000.f;
		S.Dollars = 2000000.f;
		S.MinImpulse = 1500.f;
		S.bExpensive = true;
		SpawnProp(S, FVector(150, -150, 50));
	}

	for (const FVector2D& P : { FVector2D(-40, -100), FVector2D(350, -270), FVector2D(-200, -230) })
	{
		Dyn(TEXT("Light Stand"), TEXT("LightStand"), TEXT("Cylinder"), FVector(P.X, P.Y, 0), FVector(16, 16, 230), Steel, 8.f, EChainCategory::Lighting, 150.f, 800.f)->Spec.bMovable = true;
	}
	Dyn(TEXT("Ladder"), TEXT("Ladder"), TEXT("Cube"), FVector(480, -250, 0), FVector(55, 8, 250), FLinearColor(0.95f, 0.75f, 0.15f), 10.f, EChainCategory::Hazard, 120.f, 800.f)->Spec.bMovable = true;
	const FLinearColor CanColors[] = { FLinearColor(0.9f, 0.1f, 0.1f), FLinearColor(0.1f, 0.5f, 0.95f), FLinearColor(0.2f, 0.85f, 0.25f) };
	for (int32 i = 0; i < 3; ++i)
	{
		Dyn(TEXT("Paint Can"), TEXT("PaintCan"), TEXT("Cylinder"), FVector(360 + i * 42, -140, 0), FVector(26, 26, 30), CanColors[i], 2.f, EChainCategory::Liquid, 60.f, 400.f)->Spec.bMovable = true;
	}
	Dyn(TEXT("Wardrobe Rack"), TEXT("Rack"), TEXT("Cube"), FVector(560, -20, 0), FVector(140, 55, 195), FLinearColor(0.5f, 0.5f, 0.55f), 25.f, EChainCategory::Furniture, 200.f, 1500.f)->Spec.bMovable = true;

	// Ramp: a bowling ball placed on it rolls toward the camera dolly.
	Static(TEXT("Ramp"), TEXT("Cube"), FVector(-330, -100, 42), FVector(340, 140, 12), FLinearColor(0.85f, 0.85f, 0.9f), FRotator(-15.f, 0.f, 0.f), true);
	Static(TEXT("Ramp Stripe"), TEXT("Cube"), FVector(-330, -100, 49), FVector(340, 20, 1), FLinearColor(1.f, 0.8f, 0.1f), FRotator(-15.f, 0.f, 0.f), true);

	// --- Craft services: table, big multi-tier cake, urn, cooler ---
	Static(TEXT("Craft Table"), TEXT("Table"), FVector(800, -350, 0), FVector(230, 110, 78), FLinearColor(0.95f, 0.95f, 0.95f));
	Dyn(TEXT("Cake Tier 1"), TEXT("CakeTier"), TEXT("Cylinder"), FVector(790, -350, 78), FVector(90, 90, 24), FLinearColor(1.f, 0.45f, 0.65f), 3.f, EChainCategory::Food, 250.f, 300.f);
	Dyn(TEXT("Cake Tier 2"), TEXT("CakeTier"), TEXT("Cylinder"), FVector(790, -350, 102), FVector(62, 62, 24), FLinearColor(1.f, 0.62f, 0.78f), 2.f, EChainCategory::Food, 250.f, 300.f);
	Dyn(TEXT("Cake Tier 3"), TEXT("CakeTop"), TEXT("Cylinder"), FVector(790, -350, 126), FVector(40, 40, 24), FLinearColor(1.f, 0.78f, 0.88f), 1.f, EChainCategory::Food, 250.f, 300.f);
	Dyn(TEXT("Coffee Urn"), TEXT("Urn"), TEXT("Cylinder"), FVector(880, -350, 78), FVector(34, 34, 52), Steel, 6.f, EChainCategory::Liquid, 150.f, 600.f);
	Dyn(TEXT("Water Cooler"), TEXT("Cooler"), TEXT("Cylinder"), FVector(950, -210, 0), FVector(40, 40, 110), FLinearColor(0.95f, 0.95f, 0.95f), 10.f, EChainCategory::Liquid, 200.f, 800.f);

	// --- Prop shelf (right): frame, barrels, hat boxes, cacti ---
	Static(TEXT("Shelf Back"), TEXT("Cube"), FVector(950, 650, 0), FVector(280, 6, 250), FLinearColor(0.25f, 0.13f, 0.06f));
	Static(TEXT("Shelf Side L"), TEXT("Cube"), FVector(815, 600, 0), FVector(10, 60, 250), Wood);
	Static(TEXT("Shelf Side R"), TEXT("Cube"), FVector(1085, 600, 0), FVector(10, 60, 250), Wood);
	Static(TEXT("Shelf Board Mid"), TEXT("Cube"), FVector(950, 600, 60), FVector(280, 60, 6), Wood);
	Static(TEXT("Shelf Board High"), TEXT("Cube"), FVector(950, 600, 150), FVector(280, 60, 6), Wood);
	for (int32 i = 0; i < 4; ++i)
	{
		Dyn(TEXT("Barrel"), TEXT("Barrel"), TEXT("Cylinder"), FVector(845 + i * 62, 600, 66), FVector(44, 44, 80), FLinearColor(0.55f, 0.3f, 0.12f), 12.f, EChainCategory::Furniture, 100.f, 800.f);
	}
	const FLinearColor HatColors[] = { FLinearColor(0.95f, 0.85f, 0.6f), FLinearColor(0.6f, 0.75f, 0.95f), FLinearColor(0.95f, 0.6f, 0.7f) };
	for (int32 i = 0; i < 3; ++i)
	{
		Dyn(TEXT("Hat Box"), TEXT("HatBox"), TEXT("Cylinder"), FVector(845 + i * 70, 600, 156), FVector(42, 42, 30), HatColors[i], 1.5f, EChainCategory::Furniture, 80.f, 300.f);
	}
	for (int32 i = 0; i < 2; ++i)
	{
		Dyn(TEXT("Fake Cactus"), TEXT("Cactus"), TEXT("Cylinder"), FVector(1040 + i * 28, 600, 156), FVector(34, 34, 80), FLinearColor(0.2f, 0.65f, 0.28f), 2.f, EChainCategory::Furniture, 90.f, 400.f);
	}

	// --- Cue devices: held payloads and effect machines ---
	auto Held = [this](const TCHAR* Name, const TCHAR* Kind, const TCHAR* Shape, FVector Bottom, FVector DimsCm, FLinearColor Color, float Mass, EChainCategory Cat, float Value)
	{
		FPropSpec S;
		S.Name = Name;
		S.Kind = Kind;
		S.Shape = Shape;
		S.Scale = DimsCm / 100.0;
		S.Color = Color;
		S.bDynamic = true;
		S.bTracked = true;
		S.MassKg = Mass;
		S.Category = Cat;
		S.Value = Value;
		S.MinImpulse = 600.f;
		S.bCanOrigin = true;
		S.bSimulateInTake = false;   // Stays hanging until its cue fires.
		return SpawnProp(S, Bottom);
	};

	ACueDeviceActor* SandbagA = SpawnDevice(ECueType::Sandbag, TEXT("Sandbag A"), FVector(-40, -100, 500), FVector(0.45, 0.3, 0.2), FLinearColor(0.5f, 0.5f, 0.55f), TEXT("Winch"));
	SandbagA->Payload = Held(TEXT("Sandbag A"), TEXT("Sandbag"), TEXT("Cube"), FVector(-40, -100, 420), FVector(46, 30, 30), FLinearColor(0.82f, 0.7f, 0.42f), 15.f, EChainCategory::Hazard, 200.f);

	ACueDeviceActor* SandbagB = SpawnDevice(ECueType::Sandbag, TEXT("Sandbag B"), FVector(560, -20, 500), FVector(0.45, 0.3, 0.2), FLinearColor(0.5f, 0.5f, 0.55f), TEXT("Winch"));
	SandbagB->Payload = Held(TEXT("Sandbag B"), TEXT("Sandbag"), TEXT("Cube"), FVector(560, -20, 420), FVector(46, 30, 30), FLinearColor(0.82f, 0.7f, 0.42f), 15.f, EChainCategory::Hazard, 200.f);

	ACueDeviceActor* Chandelier = SpawnDevice(ECueType::Chandelier, TEXT("Chandelier Winch"), FVector(-780, 300, 560), FVector(0.4, 0.3, 0.25), FLinearColor(0.5f, 0.5f, 0.55f), TEXT("Winch"));
	Chandelier->Payload = Held(TEXT("Chandelier"), TEXT("Chandelier"), TEXT("Cube"), FVector(-780, 300, 440), FVector(100, 100, 30), Gold, 60.f, EChainCategory::Lighting, 500.f);

	SpawnDevice(ECueType::Pyro, TEXT("Pyro Puff"), FVector(350, 250, 0), FVector(0.6, 0.6, 0.5), FLinearColor(0.75f, 0.1f, 0.08f), TEXT("Pyro"));
	if (ACueDeviceActor* Wind = SpawnDevice(ECueType::Wind, TEXT("Wind Machine"), FVector(550, -650, 0), FVector(0.3, 1.3, 1.3), FLinearColor(0.35f, 0.8f, 0.9f), TEXT("Fan"), 90.f))
	{
		Wind->Strength = 30000.f;
	}

	// Hanging payloads are tracked but must not move until their cue fires.
	for (ATake37PropActor* P : Props)
	{
		if (P && !P->Spec.bSimulateInTake)
		{
			P->SetPhysicsActive(false);
		}
	}
}

void ATake37Stage::BuildCast()
{
	auto Step = [](float X, float Y, float Wait, float Speed) { FRouteStep S; S.Mark = FVector(X, Y, 0); S.Wait = Wait; S.Speed = Speed; return S; };
	TArray<FStageActorSpec> Cast;

	FStageActorSpec Brick;
	Brick.Id = TEXT("brick");
	Brick.BarkId = TEXT("Brick");
	Brick.Traits = { 0.9f, 0.6f, 0.1f, 0.3f, 0.4f, 1.0f, TEXT("Dame Vivienne Sterling"), 0.8f };
	Brick.Name = TEXT("Brick Hardcastle");
	Brick.Role = TEXT("Leading Man");
	Brick.Color = FLinearColor(0.3f, 0.45f, 0.8f);
	Brick.Skin = FLinearColor(0.97f, 0.72f, 0.55f);
	Brick.Scale = 1.7f;
	Brick.Route = { Step(-260, -420, 2.f, 150), Step(150, -520, 2.5f, 150), Step(560, -520, 3.f, 150) };
	Cast.Add(Brick);

	FStageActorSpec Viv;
	Viv.Id = TEXT("vivienne");
	Viv.BarkId = TEXT("Vivienne");
	Viv.Traits = { 0.3f, 1.0f, 0.5f, 0.0f, 0.3f, 0.8f, TEXT("Brick Hardcastle"), 0.6f };
	Viv.Name = TEXT("Dame Vivienne Sterling");
	Viv.Role = TEXT("Diva");
	Viv.Color = FLinearColor(0.45f, 0.1f, 0.6f);
	Viv.Skin = FLinearColor(0.98f, 0.8f, 0.7f);
	Viv.Scale = 1.6f;
	Viv.Route = { Step(-700, 40, 2.f, 120), Step(-500, -420, 2.f, 120), Step(-100, -520, 3.f, 120) };
	Cast.Add(Viv);

	FStageActorSpec Gus;
	Gus.Id = TEXT("gus");
	Gus.BarkId = TEXT("Gus");
	Gus.Traits = { 0.1f, 0.3f, 0.9f, 0.9f, 0.8f, 0.0f, TEXT(""), 0.f };
	Gus.Name = TEXT("Gus Pickles");
	Gus.Role = TEXT("Production Assistant");
	Gus.Color = FLinearColor(0.35f, 0.38f, 0.42f);
	Gus.Skin = FLinearColor(1.f, 0.78f, 0.65f);
	Gus.Scale = 1.5f;
	Gus.Route = { Step(560, -520, 1.f, 300), Step(150, -520, 1.f, 300), Step(-260, -420, 1.f, 300), Step(-700, 40, 2.f, 300) };
	Cast.Add(Gus);

	const FVector Starts[] = { FVector(-420, -470, 160), FVector(-640, -40, 160), FVector(300, -560, 160) };
	for (int32 i = 0; i < Cast.Num(); ++i)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		const FRotator Face(0.f, i == 2 ? 180.f : 0.f, 0.f);
		if (AStageActorCharacter* A = GetWorld()->SpawnActor<AStageActorCharacter>(Starts[i], Face, Params))
		{
			A->Setup(Cast[i]);
			Actors.Add(A);
		}
	}
}
