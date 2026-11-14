#include "UI/Take37HUD.h"
#include "AI/BarkSubsystem.h"
#include "Actors/StageActorCharacter.h"
#include "Chain/ChainPropComponent.h"
#include "Chain/ChainReactionSubsystem.h"
#include "Chain/CueDeviceActor.h"
#include "Core/CartCatalog.h"
#include "Core/ChallengeDefinition.h"
#include "Core/TakeDirectorSubsystem.h"
#include "Player/DirectorPawn.h"
#include "Player/PlacementComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/Font.h"
#include "Engine/FontFace.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "Take37.h"

namespace
{
	// Palette: warm cream paper, ink outlines, punchy accents.
	const FLinearColor Cream(0.99f, 0.95f, 0.84f);
	const FLinearColor Ink(0.08f, 0.07f, 0.1f);
	const FLinearColor Yellow(1.f, 0.8f, 0.18f);
	const FLinearColor Red(0.9f, 0.2f, 0.18f);
	const FLinearColor Green(0.2f, 0.68f, 0.34f);
	const FLinearColor Blue(0.24f, 0.4f, 0.85f);
	const FLinearColor Orange(0.98f, 0.5f, 0.14f);
	const FLinearColor Pink(0.95f, 0.35f, 0.65f);
	const FLinearColor Shadow(0.f, 0.f, 0.f, 0.38f);

	FString Money(int64 Amount)
	{
		return TEXT("$") + FText::AsNumber(Amount).ToString();
	}

	UFont* MakeRuntimeFont(UObject* Outer, const TCHAR* FacePath, int32 Size)
	{
		UFontFace* Face = LoadObject<UFontFace>(nullptr, FacePath);
		if (!Face)
		{
			UE_LOG(LogTake37, Warning, TEXT("Font face %s missing; falling back to the engine font. Run Tools/Editor/setup_take37.py."), FacePath);
			return nullptr;
		}
		UFont* Font = NewObject<UFont>(Outer);
		Font->FontCacheType = EFontCacheType::Runtime;
		Font->LegacyFontSize = Size;
		Font->LegacyFontName = TEXT("Default");
		FTypefaceEntry Entry(TEXT("Default"));
		Entry.Font = FFontData(Face);
		Font->GetMutableInternalCompositeFont().DefaultTypeface.Fonts.Add(Entry);
		return Font;
	}
}

void ATake37HUD::BeginPlay()
{
	Super::BeginPlay();
	HeaderFont = MakeRuntimeFont(this, TEXT("/Game/UI/Fonts/FF_Slackey.FF_Slackey"), 38);
	BodyFont = MakeRuntimeFont(this, TEXT("/Game/UI/Fonts/FF_Englebert.FF_Englebert"), 40);

	if (UWorld* World = GetWorld())
	{
		BoundChain = World->GetSubsystem<UChainReactionSubsystem>();
		BoundBarks = World->GetSubsystem<UBarkSubsystem>();
		if (BoundChain.IsValid())
		{
			BoundChain->OnLink.AddUObject(this, &ATake37HUD::HandleLink);
		}
		if (BoundBarks.IsValid())
		{
			BoundBarks->OnBark.AddUObject(this, &ATake37HUD::HandleBark);
		}
	}
}

void ATake37HUD::HandleLink(const FChainLink& Link)
{
	const double Now = GetWorld()->GetTimeSeconds();
	FFloatingLabel L;
	L.Location = Link.ToLocation + FVector(0, 0, 90);
	L.Born = Now;
	L.Color = Link.bImprov ? Pink : Yellow;
	const float DepthMult = 1.f + 0.5f * Link.Depth;
	L.Text = (Link.LinkType == EChainLinkType::Origin)
		? FString::Printf(TEXT("+%d %s!"), FMath::RoundToInt(Link.Score), *Link.ToName.ToString())
		: FString::Printf(TEXT("+%d %s x%.1f"), FMath::RoundToInt(Link.Score), *Link.ToName.ToString(), DepthMult);
	Floating.Add(L);

	LinkFeed.Add(FString::Printf(TEXT("%d. %s > %s  +%d"), Link.Depth, *Link.FromName.ToString(), *Link.ToName.ToString(), FMath::RoundToInt(Link.Score)));
	if (LinkFeed.Num() > 5)
	{
		LinkFeed.RemoveAt(0);
	}
}

void ATake37HUD::HandleBark(FName Actor, const FString& InSubtitle, int32 Intensity)
{
	Subtitle = InSubtitle;
	SubtitleActor = Actor;
	SubtitleUntil = GetWorld()->GetRealTimeSeconds() + 3.0 + Intensity * 0.3;
}

FName ATake37HUD::HitTestButton(const FVector2D& Point) const
{
	for (const FButton& B : Buttons)
	{
		if (B.Rect.IsInside(Point))
		{
			return B.Id;
		}
	}
	return NAME_None;
}

UFont* ATake37HUD::GetFont(EFont Font) const
{
	UFont* F = (Font == EFont::Header) ? HeaderFont.Get() : BodyFont.Get();
	return F ? F : GEngine->GetLargeFont();
}

float ATake37HUD::TextWidth(const FString& Text, float Size, EFont Font) const
{
	float W = 0.f, H = 0.f;
	const_cast<ATake37HUD*>(this)->GetTextSize(Text, W, H, GetFont(Font), Size * UI);
	return W;
}

float ATake37HUD::TextHeight(float Size, EFont Font) const
{
	float W = 0.f, H = 0.f;
	const_cast<ATake37HUD*>(this)->GetTextSize(TEXT("Ag"), W, H, GetFont(Font), Size * UI);
	return H;
}

float ATake37HUD::Label(const FString& Text, float X, float Y, const FLinearColor& Color, float Size, EFont Font, int32 Align, bool bShadow)
{
	const float W = TextWidth(Text, Size, Font);
	if (Align == 1)
	{
		X -= W * 0.5f;
	}
	else if (Align == 2)
	{
		X -= W;
	}
	if (bShadow)
	{
		const float S = FMath::Max(2.f, (Font == EFont::Header ? 3.f : 2.f) * UI);
		DrawText(Text, Ink, X + S, Y + S, GetFont(Font), Size * UI);
	}
	DrawText(Text, Color, X, Y, GetFont(Font), Size * UI);
	return TextHeight(Size, Font);
}

float ATake37HUD::Wrapped(const FString& Text, float X, float Y, float MaxWidth, const FLinearColor& Color, float Size, EFont Font, int32 Align, bool bShadow)
{
	TArray<FString> Words;
	Text.ParseIntoArray(Words, TEXT(" "));
	FString Line;
	float Cursor = Y;
	const float LineH = TextHeight(Size, Font) * 1.08f;
	auto Flush = [&]()
	{
		if (!Line.IsEmpty())
		{
			const float DrawX = (Align == 1) ? X + MaxWidth * 0.5f : (Align == 2 ? X + MaxWidth : X);
			Label(Line, DrawX, Cursor, Color, Size, Font, Align, bShadow);
			Cursor += LineH;
			Line.Reset();
		}
	};
	for (const FString& Word : Words)
	{
		const FString Candidate = Line.IsEmpty() ? Word : Line + TEXT(" ") + Word;
		if (TextWidth(Candidate, Size, Font) > MaxWidth && !Line.IsEmpty())
		{
			Flush();
			Line = Word;
		}
		else
		{
			Line = Candidate;
		}
	}
	Flush();
	return Cursor - Y;
}

void ATake37HUD::RRect(float X, float Y, float W, float H, float R, const FLinearColor& Color)
{
	R = FMath::Min(R, FMath::Min(W, H) * 0.5f);
	// Body: one full-height centre strip, then scanline rows for the rounded ends.
	DrawRect(Color, X + R, Y, W - 2.f * R, H);
	const int32 Rows = FMath::Max(1, FMath::CeilToInt(R / 2.f));
	const float RowH = R / Rows;
	for (int32 i = 0; i < Rows; ++i)
	{
		const float Dy = R - (i + 0.5f) * RowH;                       // distance from the corner centre line
		const float Inset = R - FMath::Sqrt(FMath::Max(0.f, R * R - Dy * Dy));
		const float Wd = R - Inset;
		const float YTop = Y + i * RowH;
		const float YBot = Y + H - (i + 1) * RowH;
		DrawRect(Color, X + Inset, YTop, Wd, RowH + 0.5f);
		DrawRect(Color, X + W - R, YTop, Wd, RowH + 0.5f);
		DrawRect(Color, X + Inset, YBot, Wd, RowH + 0.5f);
		DrawRect(Color, X + W - R, YBot, Wd, RowH + 0.5f);
	}
	DrawRect(Color, X, Y + R, R, H - 2.f * R);
	DrawRect(Color, X + W - R, Y + R, R, H - 2.f * R);
}

void ATake37HUD::Card(float X, float Y, float W, float H, const FLinearColor& Fill, bool bClapper)
{
	const float O = 5.f * UI, S = 9.f * UI, R = 20.f * UI;
	RRect(X + S, Y + S, W, H, R, Shadow);
	RRect(X - O, Y - O, W + 2.f * O, H + 2.f * O, R + O, Ink);
	RRect(X, Y, W, H, R, Fill);
	if (bClapper)
	{
		// Clapperboard stripes along the top edge.
		const float StripeH = 22.f * UI, StripeW = 38.f * UI;
		const int32 N = FMath::Max(1, FMath::FloorToInt((W - 2.f * R) / StripeW));
		DrawRect(Ink, X + R - 3.f * UI, Y + 3.f * UI, N * StripeW + 6.f * UI, StripeH + 6.f * UI);
		for (int32 i = 0; i < N; ++i)
		{
			DrawRect((i % 2 == 0) ? Yellow : Ink, X + R + i * StripeW, Y + 6.f * UI, StripeW, StripeH);
		}
	}
}

void ATake37HUD::Bulbs(float X, float Y, float W)
{
	const float Step = 34.f * UI;
	const int32 N = FMath::Max(2, FMath::FloorToInt(W / Step));
	const float Gap = W / N;
	for (int32 i = 0; i < N; ++i)
	{
		const FVector2D C(X + Gap * (i + 0.5f), Y);
		const bool bOn = (i % 2 == 0) == (FMath::FloorToInt(GetWorld()->GetRealTimeSeconds() * 2.f) % 2 == 0);
		RRect(C.X - 9.f * UI, C.Y - 9.f * UI, 18.f * UI, 18.f * UI, 9.f * UI, Ink);
		RRect(C.X - 6.5f * UI, C.Y - 6.5f * UI, 13.f * UI, 13.f * UI, 6.5f * UI, bOn ? Yellow : FLinearColor(0.7f, 0.55f, 0.15f));
	}
}

FVector2D ATake37HUD::Plate(const FString& Text, float X, float Y, float Size, EFont Font, int32 Align, const FLinearColor& Fill, const FLinearColor& TextColor, float Pad)
{
	const float P = Pad * UI;
	const float W = TextWidth(Text, Size, Font) + P * 2.4f;
	const float H = TextHeight(Size, Font) + P * 1.1f;
	float DrawX = X;
	if (Align == 1)
	{
		DrawX -= W * 0.5f;
	}
	else if (Align == 2)
	{
		DrawX -= W;
	}
	const float O = 3.5f * UI;
	RRect(DrawX + 5.f * UI, Y + 5.f * UI, W, H, H * 0.5f, Shadow);
	RRect(DrawX - O, Y - O, W + 2.f * O, H + 2.f * O, H * 0.5f + O, Ink);
	RRect(DrawX, Y, W, H, H * 0.5f, Fill);
	Label(Text, DrawX + P * 1.2f, Y + P * 0.5f, TextColor, Size, Font, 0, false);
	return FVector2D(W, H);
}

bool ATake37HUD::Button(FName Id, const FString& Text, float X, float Y, float W, float H, const FLinearColor& Fill, bool bEnabled, bool bActive, float Size)
{
	const float O = 5.f * UI, R = 18.f * UI;
	FLinearColor C = bEnabled ? Fill : FLinearColor(0.55f, 0.53f, 0.5f);
	RRect(X + 7.f * UI, Y + 9.f * UI, W, H, R, Shadow);
	if (bActive)
	{
		RRect(X - O - 5.f * UI, Y - O - 5.f * UI, W + 2.f * (O + 5.f * UI), H + 2.f * (O + 5.f * UI), R + O + 5.f * UI, Yellow);
	}
	RRect(X - O, Y - O, W + 2.f * O, H + 2.f * O, R + O, Ink);
	RRect(X, Y, W, H, R, C);
	RRect(X + 6.f * UI, Y + 5.f * UI, W - 12.f * UI, H * 0.38f, R * 0.7f, FLinearColor(1.f, 1.f, 1.f, bEnabled ? 0.22f : 0.08f));

	// Shrink to fit the button.
	float S = Size;
	while (TextWidth(Text, S, EFont::Header) > W * 0.88f && S > 0.3f)
	{
		S *= 0.93f;
	}
	const float TH = TextHeight(S, EFont::Header);
	Label(Text, X + W * 0.5f, Y + (H - TH) * 0.5f, bEnabled ? FLinearColor::White : FLinearColor(0.85f, 0.83f, 0.8f), S, EFont::Header, 1, true);
	if (bEnabled)
	{
		PendingButtons.Add({ Id, FBox2D(FVector2D(X, Y), FVector2D(X + W, Y + H)) });
	}
	return bEnabled;
}

void ATake37HUD::DrawHUD()
{
	Super::DrawHUD();
	UWorld* World = GetWorld();
	UTakeDirectorSubsystem* Dir = World ? World->GetSubsystem<UTakeDirectorSubsystem>() : nullptr;
	UChainReactionSubsystem* Chain = World ? World->GetSubsystem<UChainReactionSubsystem>() : nullptr;
	if (!Dir || !Chain || !Canvas)
	{
		return;
	}
	UI = FMath::Max(0.5f, Canvas->ClipY / 1080.f * 0.8f);
	PendingButtons.Reset();

	const ADirectorPawn* Pawn = Cast<ADirectorPawn>(GetOwningPawn());
	UPlacementComponent* Placement = Pawn ? Pawn->GetPlacement() : nullptr;

	if (Dir->GetPhase() != ETake37Phase::Results)
	{
		DrawWorldLabels(Dir);
	}

	switch (Dir->GetPhase())
	{
	case ETake37Phase::Setup:
		DrawSetup(Dir, Placement);
		break;
	case ETake37Phase::Take:
		DrawTake(Dir, Chain);
		break;
	case ETake37Phase::Cut:
		DrawTake(Dir, Chain);
		Label(TEXT("Cut!"), Canvas->ClipX * 0.5f, Canvas->ClipY * 0.3f, Red, SizeHuge, EFont::Header, 1, true);
		break;
	case ETake37Phase::Results:
		DrawResults(Dir);
		break;
	}
	DrawFloatingLabels();
	if (Dir->GetPhase() != ETake37Phase::Results)
	{
		DrawSubtitle();
	}

	Buttons = PendingButtons;
}

void ATake37HUD::DrawWorldLabels(UTakeDirectorSubsystem* Dir)
{
	APlayerController* PC = GetOwningPlayerController();
	if (!PC || !PC->PlayerCameraManager)
	{
		return;
	}
	const FVector CamLoc = PC->PlayerCameraManager->GetCameraLocation();
	const FVector CamFwd = PC->PlayerCameraManager->GetActorForwardVector();
	auto Visible = [&](const FVector& L) { return FVector::DotProduct(L - CamLoc, CamFwd) > 0.0; };

	// The cast, so the player always sees who is who.
	for (TActorIterator<AStageActorCharacter> It(GetWorld()); It; ++It)
	{
		const FVector Loc = It->GetActorLocation() + FVector(0, 0, 130);
		if (Visible(Loc))
		{
			const FVector P = Project(Loc);
			Plate(It->DisplayName, P.X, P.Y - 28.f * UI, SizeSmall * 0.9f, EFont::Header, 1, Yellow, Ink, 9.f);
		}
	}

	// Cue devices: show which key fires them.
	for (TActorIterator<ACueDeviceActor> It(GetWorld()); It; ++It)
	{
		const ACueDeviceActor* D = *It;
		int32 Slot = INDEX_NONE;
		for (int32 i = 0; i < UTakeDirectorSubsystem::NumCueSlots; ++i)
		{
			if (Dir->GetCueDevice(i) == D)
			{
				Slot = i;
			}
		}
		const FVector Loc = D->GetActorLocation() + FVector(0, 0, 90);
		if (!Visible(Loc))
		{
			continue;
		}
		const FVector P = Project(Loc);
		const FString Text = (Slot != INDEX_NONE) ? FString::Printf(TEXT("%d  %s%s"), Slot + 1, *D->DisplayName, D->bFired ? TEXT(" (Used)") : TEXT("")) : D->DisplayName;
		Plate(Text, P.X, P.Y - 20.f * UI, SizeSmall, EFont::Header, 1, Slot != INDEX_NONE ? FLinearColor(0.62f, 0.85f, 1.f) : Cream, Ink, 9.f);
	}

	// Key set pieces so the player always knows the targets.
	if (UChainReactionSubsystem* Chain = GetWorld()->GetSubsystem<UChainReactionSubsystem>())
	{
		for (const TWeakObjectPtr<UChainPropComponent>& Prop : Chain->GetProps())
		{
			const UChainPropComponent* C = Prop.Get();
			if (!C || !C->GetOwner())
			{
				continue;
			}
			const FString Name = C->GetLabel();
			FString Text;
			FLinearColor Fill = Yellow;
			float Lift = 120.f;
			if (Name.Contains(TEXT("Hero Camera")))
			{
				Text = TEXT("$2M Hero Camera");
				Fill = Red;
				Lift = 130.f;
			}
			else if (Name == TEXT("Cake Tier 3"))
			{
				Text = TEXT("Cake");
				Fill = Pink;
				Lift = 80.f;
			}
			else
			{
				continue;
			}
			const FVector Loc = C->GetOwner()->GetActorLocation() + FVector(0, 0, Lift);
			if (Visible(Loc))
			{
				const FVector P = Project(Loc);
				Plate(Text, P.X, P.Y - 20.f * UI, SizeSmall, EFont::Header, 1, Fill, FLinearColor::White, 9.f);
			}
		}
	}
}

void ATake37HUD::DrawCue(UTakeDirectorSubsystem* Dir, bool bLive, float BottomY)
{
	const float W = 400.f * UI, H = 74.f * UI, Gap = 22.f * UI;
	const float X = Canvas->ClipX - W - 40.f * UI;
	float Y = BottomY - 3.f * (H + Gap);
	Plate(bLive ? TEXT("Director Cues") : TEXT("Cues"), X + W * 0.5f, Y - 62.f * UI, SizeSmall, EFont::Header, 1, Yellow);
	for (int32 i = 0; i < UTakeDirectorSubsystem::NumCueSlots; ++i)
	{
		const ACueDeviceActor* Device = Dir->GetCueDevice(i);
		FString Text = FString::Printf(TEXT("%d  %s"), i + 1, Device ? *Device->DisplayName : TEXT("Empty"));
		const bool bUsed = Device && Device->bFired;
		if (bUsed)
		{
			Text += TEXT(" (Used)");
		}
		const bool bEnabled = bLive ? (Device && !bUsed) : true;
		Button(FName(*FString::Printf(TEXT("Cue_%d"), i)), Text, X, Y, W, H, Blue, bEnabled, false, SizeBody);
		Y += H + Gap;
	}
}

void ATake37HUD::DrawSetup(UTakeDirectorSubsystem* Dir, UPlacementComponent* Placement)
{
	const UChallengeDefinition* Ch = Dir->GetChallenge();
	const float M = 44.f * UI;
	const float Pad = 26.f * UI;

	// Call sheet card
	const float CardW = 820.f * UI;
	float Y = M + 38.f * UI;
	const float HeadH = TextHeight(SizeHead, EFont::Header);
	const float BodyH = TextHeight(SizeBody, EFont::Body);
	const float SmallH = TextHeight(SizeSmall, EFont::Body);
	const float CardH = 38.f * UI + HeadH + BodyH * 1.2f + BodyH * 2.3f + SmallH * 1.2f * 3.f + Pad * 1.5f;
	Card(M, M, CardW, CardH, Cream, true);
	Y += Label(FString::Printf(TEXT("Call Sheet - Take %d"), Dir->GetTakeNumber()), M + Pad, Y, Orange, SizeHead, EFont::Header, 0, true) + 6.f * UI;
	Y += Label(Ch->SceneName, M + Pad, Y, Ink, SizeBody, EFont::Body) * 1.2f;
	Y += Wrapped(Ch->ObjectiveText, M + Pad, Y, CardW - Pad * 2.f, Ink, SizeBody, EFont::Body) + 10.f * UI;
	Y += Label(FString::Printf(TEXT("1 star: hit the camera with a %d+ link chain"), Ch->MinChainForObjective), M + Pad, Y, Ink, SizeSmall, EFont::Body) * 1.2f;
	Y += Label(FString::Printf(TEXT("2 stars: also score over %s"), *FText::AsNumber(Ch->Star2Score).ToString()), M + Pad, Y, Ink, SizeSmall, EFont::Body) * 1.2f;
	Y += Label(FString::Printf(TEXT("3 stars: also a chain of %d+ links"), Ch->Star3Chain), M + Pad, Y, Ink, SizeSmall, EFont::Body) * 1.2f;

	// Budget and Action!
	const int32 Remaining = Placement ? Placement->GetRemaining() : Ch->SabotageBudget;
	Plate(FString::Printf(TEXT("Budget  $%d / $%d"), Remaining, Ch->SabotageBudget), Canvas->ClipX - M, M, SizeHead, EFont::Header, 2, Remaining > 0 ? Yellow : Red, Ink, 14.f);
	Button(TEXT("Action"), TEXT("Action!"), Canvas->ClipX - 440.f * UI - M, M + 110.f * UI, 440.f * UI, 110.f * UI, Red, true, false, SizeTitle);

	// Help strip
	const float BarH = 96.f * UI;
	Card(M, Canvas->ClipY - BarH - 30.f * UI, Canvas->ClipX - M * 2.f, BarH, Cream, false);
	Wrapped(TEXT("Place items, press Space for Action!, then fire cues 1-3 to start the chain.  Click: place, select, drag.  Q / E: rotate.  Del: remove.  WASD: pan.  Right-drag: orbit.  Wheel: zoom."),
		M + Pad, Canvas->ClipY - BarH - 30.f * UI + 14.f * UI, Canvas->ClipX - M * 2.f - Pad * 2.f, Ink, SizeSmall, EFont::Body, 1);

	// Prop cart
	const float BW = 330.f * UI, BH = 96.f * UI, Gap = 26.f * UI;
	const int32 Count = Ch->AvailableItems.Num();
	float X = (Canvas->ClipX - ((BW + Gap) * Count - Gap)) * 0.5f - 200.f * UI;
	const float CartY = Canvas->ClipY - BarH - 30.f * UI - BH - 70.f * UI;
	const FVector2D CartPlate = Plate(TEXT("Prop Cart"), X, CartY - 76.f * UI, SizeSmall, EFont::Header, 0, Yellow);
	Label(TEXT("Click an item, then click the floor."), X + CartPlate.X + 24.f * UI, CartY - 66.f * UI, FLinearColor::White, SizeSmall, EFont::Body, 0, true);
	for (ECartItem Item : Ch->AvailableItems)
	{
		const FCartItemInfo& Info = Take37Cart::Get(Item);
		const bool bAfford = Info.Cost <= Remaining;
		const bool bArmed = Placement && Placement->GetArmed() == Item;
		Button(FName(*FString::Printf(TEXT("Cart_%d"), static_cast<int32>(Item))), FString::Printf(TEXT("%s $%d"), *Info.Name, Info.Cost), X, CartY, BW, BH, Orange, bAfford || bArmed, bArmed, SizeBody);
		X += BW + Gap;
	}

	DrawCue(Dir, false, CartY - 90.f * UI);
}

void ATake37HUD::DrawTake(UTakeDirectorSubsystem* Dir, UChainReactionSubsystem* Chain)
{
	const float M = 44.f * UI;
	const float Bar = Canvas->ClipY * 0.07f;

	// Letterbox bars (GDD section 8.2)
	DrawRect(FLinearColor::Black, 0.f, 0.f, Canvas->ClipX, Bar);
	DrawRect(FLinearColor::Black, 0.f, Canvas->ClipY - Bar, Canvas->ClipX, Bar);

	const float Top = Bar + 22.f * UI;
	const float TimeLeft = FMath::Max(0.f, Dir->GetTakeTimeLimit() - Dir->GetTakeTime());
	Plate(FString::Printf(TEXT("Take %d  -  %.0f s"), Dir->GetTakeNumber(), TimeLeft), M, Top, SizeHead, EFont::Header, 0, Cream);

	const FVector2D Score = Plate(FString::Printf(TEXT("Box Office  %s"), *FText::AsNumber(FMath::RoundToInt(Chain->GetTotalScore())).ToString()), Canvas->ClipX - M, Top, SizeHead, EFont::Header, 2, Yellow);
	Plate(FString::Printf(TEXT("Damages  %s"), *Money(static_cast<int64>(Chain->GetDamages()))), Canvas->ClipX - M, Top + Score.Y + 18.f * UI, SizeBody, EFont::Header, 2, Red, FLinearColor::White);

	if (Dir->GetPhase() == ETake37Phase::Take && Chain->GetLinkCount() == 0)
	{
		// Nothing moves until a cue fires, so say so loudly.
		const float Pulse = 0.5f + 0.5f * FMath::Sin(GetWorld()->GetRealTimeSeconds() * 6.f);
		Plate(TEXT("Fire A Cue!  Press 1, 2 Or 3"), Canvas->ClipX * 0.5f, Canvas->ClipY * 0.42f, SizeTitle, EFont::Header, 1, FMath::Lerp(Yellow, Orange, Pulse), Ink, 20.f);
	}
	if (Chain->GetBestChainLinks() > 0)
	{
		const FVector2D C = Plate(FString::Printf(TEXT("Chain x%d"), Chain->GetBestChainLinks()), Canvas->ClipX * 0.5f, Top, SizeTitle, EFont::Header, 1, Cream, Ink, 14.f);
		if (Chain->GetComboMultiplier() > 1.01f)
		{
			Plate(FString::Printf(TEXT("Combo x%.2f"), Chain->GetComboMultiplier()), Canvas->ClipX * 0.5f, Top + C.Y + 14.f * UI, SizeHead, EFont::Header, 1, Yellow);
		}
	}

	// Last links (debug-friendly feed, GDD section 12.5)
	float Y = Top + 150.f * UI;
	for (const FString& Line : LinkFeed)
	{
		Y += Plate(Line, M, Y, SizeSmall, EFont::Body, 0, Cream, Ink, 9.f).Y + 10.f * UI;
	}

	if (Dir->GetPhase() == ETake37Phase::Take)
	{
		const float BottomY = Canvas->ClipY - Bar - 50.f * UI;
		DrawCue(Dir, true, BottomY);
		const bool bCan = Dir->GetTakeTime() >= 5.f;
		Button(TEXT("Cut"), bCan ? TEXT("Cut!") : TEXT("Cut (After 5 S)"), Canvas->ClipX - 400.f * UI - 40.f * UI,
			BottomY - 3.f * (74.f + 22.f) * UI - 190.f * UI, 400.f * UI, 90.f * UI, Red, bCan, false, SizeHead);
	}
}

void ATake37HUD::DrawResults(UTakeDirectorSubsystem* Dir)
{
	const FTakeResults& R = Dir->GetResults();
	const float W = FMath::Min(1480.f * UI, Canvas->ClipX - 120.f * UI);
	const float H = FMath::Min(1130.f * UI, Canvas->ClipY - 60.f * UI);
	const float X = (Canvas->ClipX - W) * 0.5f, Y0 = (Canvas->ClipY - H) * 0.5f;
	const float Pad = 44.f * UI;
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.6f), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY);
	Card(X, Y0, W, H, Cream, true);
	Bulbs(X + 30.f * UI, Y0 + 52.f * UI, W - 60.f * UI);

	float Y = Y0 + 76.f * UI;
	Y += Label(TEXT("Score Card"), X + W * 0.5f, Y, Orange, SizeTitle, EFont::Header, 1, true) + 4.f * UI;
	FString Stars;
	for (int32 i = 0; i < 3; ++i)
	{
		Stars += (i < R.Stars) ? TEXT("[ * ]  ") : TEXT("[   ]  ");
	}
	Y += Label(Stars, X + W * 0.5f, Y, Yellow, SizeHead, EFont::Header, 1, true) + 14.f * UI;

	Y += Label(FString::Printf(TEXT("Box Office:  %s"), *FText::AsNumber(R.Score).ToString()), X + Pad, Y, Ink, SizeHead, EFont::Header, 0, false) * 1.05f;
	Y += Label(FString::Printf(TEXT("Longest chain: %d links (%d total)"), R.BestChain, R.LinkCount), X + Pad, Y, Ink, SizeBody, EFont::Body) * 1.1f;
	Y += Label(FString::Printf(TEXT("Damages: %s"), *Money(R.Damages)), X + Pad, Y, Red, SizeBody, EFont::Body) * 1.1f;
	Y += Label(R.bHeroHit ? FString::Printf(TEXT("$2M Hero Camera: smashed at link %d"), R.HeroDepth) : FString(TEXT("$2M Hero Camera: survived")), X + Pad, Y, Ink, SizeBody, EFont::Body) * 1.3f;

	// Critic clipping
	const float ClipH = (Y0 + H) - Y - 150.f * UI;
	const float CX = X + Pad;
	const float CW = W - Pad * 2.f;
	RRect(CX, Y, CW, ClipH, 10.f * UI, Ink);
	RRect(CX + 4.f * UI, Y + 4.f * UI, CW - 8.f * UI, ClipH - 8.f * UI, 8.f * UI, FLinearColor(0.95f, 0.92f, 0.8f));
	float CY = Y + 14.f * UI;
	CY += Label(R.Publication, X + W * 0.5f, CY, Ink, SizeSmall, EFont::Header, 1, false) + 4.f * UI;
	CY += Label(R.Headline, X + W * 0.5f, CY, Ink, SizeHead, EFont::Header, 1, false) + 4.f * UI;
	CY += Label(TEXT("\"") + R.PullQuote + TEXT("\""), X + W * 0.5f, CY, Red, SizeBody, EFont::Body, 1) + 8.f * UI;
	CY += Wrapped(R.Review, CX + Pad * 0.6f, CY, CW - Pad * 1.2f, Ink, SizeSmall, EFont::Body, 1);
	Label(TEXT("- ") + R.CriticName, CX + CW - Pad * 0.6f, FMath::Min(CY + 6.f * UI, Y + ClipH - TextHeight(SizeSmall, EFont::Body) - 12.f * UI), Ink, SizeSmall, EFont::Body, 2, false);

	const float BY = Y0 + H - 118.f * UI;
	Button(TEXT("Retry"), TEXT("Retry Scene"), X + Pad, BY, 520.f * UI, 90.f * UI, Green, true, false, SizeHead);
	Button(TEXT("Next"), TEXT("Next Scene (Locked)"), X + W - Pad - 520.f * UI, BY, 520.f * UI, 90.f * UI, FLinearColor(0.5f, 0.5f, 0.5f), false, false, SizeHead);
}

void ATake37HUD::DrawFloatingLabels()
{
	APlayerController* PC = GetOwningPlayerController();
	if (!PC || !PC->PlayerCameraManager)
	{
		return;
	}
	const double Now = GetWorld()->GetTimeSeconds();
	const FVector CamLoc = PC->PlayerCameraManager->GetCameraLocation();
	const FVector CamFwd = PC->PlayerCameraManager->GetActorForwardVector();

	for (int32 i = Floating.Num() - 1; i >= 0; --i)
	{
		const FFloatingLabel& L = Floating[i];
		const double Age = Now - L.Born;
		if (Age > 2.2)
		{
			Floating.RemoveAt(i);
			continue;
		}
		if (FVector::DotProduct(L.Location - CamLoc, CamFwd) <= 0.0)
		{
			continue;
		}
		const FVector P = Project(L.Location);
		FLinearColor C = L.Color;
		C.A = static_cast<float>(1.0 - FMath::Clamp((Age - 1.4) / 0.8, 0.0, 1.0));
		const float Pop = 1.f + static_cast<float>(FMath::Clamp(0.25 - Age, 0.0, 0.25)) * 2.f;
		Label(L.Text, P.X, P.Y - static_cast<float>(Age) * 60.f * UI, C, SizeHead * Pop, EFont::Header, 1, true);
	}
}

void ATake37HUD::DrawSubtitle()
{
	if (Subtitle.IsEmpty() || GetWorld()->GetRealTimeSeconds() > SubtitleUntil)
	{
		return;
	}
	const FString Name = SubtitleActor.ToString();
	const float Y = Canvas->ClipY * 0.78f;
	const FVector2D N = Plate(Name, Canvas->ClipX * 0.5f, Y, SizeSmall, EFont::Header, 1, Yellow, Ink, 9.f);
	Plate(Subtitle, Canvas->ClipX * 0.5f, Y + N.Y + 10.f * UI, SizeHead, EFont::Body, 1, Cream, Ink, 16.f);
}
