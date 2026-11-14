using UnrealBuildTool;

public class AIMegaJam2026EditorTarget : TargetRules
{
	public AIMegaJam2026EditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("Take37");
	}
}
