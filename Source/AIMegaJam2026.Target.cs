using UnrealBuildTool;

public class AIMegaJam2026Target : TargetRules
{
	public AIMegaJam2026Target(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("Take37");
	}
}
