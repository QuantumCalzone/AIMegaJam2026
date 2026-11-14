#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "Chain/ChainTypes.h"
#include "Take37HUD.generated.h"

class UTakeDirectorSubsystem;
class UChainReactionSubsystem;
class UBarkSubsystem;
class UPlacementComponent;
class UFont;

/**
 * Canvas HUD for the whole M1 loop. Clean comedic look: cream cards with thick ink outlines and hard offset
 * shadows, clapperboard stripes, marquee bulbs, rounded buttons.
 * Headers use Slackey (Proper Case), body text uses Englebert. UMG replaces this later (GDD section 11).
 */
UCLASS()
class TAKE37_API ATake37HUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;
	virtual void DrawHUD() override;

	/** Returns the id of the button under the point, or NAME_None. Uses last frame's layout. */
	FName HitTestButton(const FVector2D& Point) const;

private:
	struct FButton
	{
		FName Id;
		FBox2D Rect;
	};
	struct FFloatingLabel
	{
		FString Text;
		FVector Location;
		double Born = 0.0;
		FLinearColor Color;
	};
	enum class EFont : uint8 { Header, Body };

	void HandleLink(const FChainLink& Link);
	void HandleBark(FName Actor, const FString& Subtitle, int32 Intensity);

	// Text sizes (multiplied by the resolution scale).
	static constexpr float SizeSmall = 0.62f;
	static constexpr float SizeBody = 0.78f;
	static constexpr float SizeHead = 1.05f;
	static constexpr float SizeTitle = 1.7f;
	static constexpr float SizeHuge = 3.6f;

	UFont* GetFont(EFont Font) const;
	float TextWidth(const FString& Text, float Size, EFont Font) const;
	float TextHeight(float Size, EFont Font) const;
	/** Draws text with a hard ink shadow. Align: 0 left, 1 centre, 2 right. Returns the line height. */
	float Label(const FString& Text, float X, float Y, const FLinearColor& Color, float Size, EFont Font, int32 Align = 0, bool bShadow = true);
	/** Word-wrapped body text; returns the total height. */
	float Wrapped(const FString& Text, float X, float Y, float MaxWidth, const FLinearColor& Color, float Size, EFont Font, int32 Align = 0, bool bShadow = false);
	/** Cream pill with text; returns its size. */
	FVector2D Plate(const FString& Text, float X, float Y, float Size, EFont Font, int32 Align = 1, const FLinearColor& Fill = FLinearColor(0.99f, 0.95f, 0.84f), const FLinearColor& TextColor = FLinearColor(0.08f, 0.07f, 0.1f), float Pad = 12.f);
	bool Button(FName Id, const FString& Text, float X, float Y, float W, float H, const FLinearColor& Fill, bool bEnabled = true, bool bActive = false, float Size = SizeBody);

	void RRect(float X, float Y, float W, float H, float Radius, const FLinearColor& Color);
	/** Cream card with ink outline and hard shadow. */
	void Card(float X, float Y, float W, float H, const FLinearColor& Fill, bool bClapper = false);
	void Bulbs(float X, float Y, float W);

	void DrawSetup(UTakeDirectorSubsystem* Dir, UPlacementComponent* Placement);
	void DrawTake(UTakeDirectorSubsystem* Dir, UChainReactionSubsystem* Chain);
	void DrawCue(UTakeDirectorSubsystem* Dir, bool bLive, float BottomY);
	void DrawResults(UTakeDirectorSubsystem* Dir);
	void DrawWorldLabels(UTakeDirectorSubsystem* Dir);
	void DrawFloatingLabels();
	void DrawSubtitle();

	UPROPERTY() TObjectPtr<UFont> HeaderFont;
	UPROPERTY() TObjectPtr<UFont> BodyFont;

	TArray<FButton> Buttons;
	TArray<FButton> PendingButtons;
	TArray<FFloatingLabel> Floating;
	TArray<FString> LinkFeed;
	FString Subtitle;
	FName SubtitleActor;
	double SubtitleUntil = 0.0;
	float UI = 1.f;

	TWeakObjectPtr<UChainReactionSubsystem> BoundChain;
	TWeakObjectPtr<UBarkSubsystem> BoundBarks;
};
