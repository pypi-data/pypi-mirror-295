import os
from dataclasses import dataclass
from importlib import resources

from pkgs.argument_parser import CachedParser
from uncountable.types import job_definition_t

profile_parser = CachedParser(job_definition_t.ProfileDefinition)


@dataclass(kw_only=True)
class ProfileDetails:
    name: str
    definition: job_definition_t.ProfileDefinition


def load_profiles() -> list[ProfileDetails]:
    profiles_module = os.environ["UNC_PROFILES_MODULE"]
    profiles = [
        entry for entry in resources.files(profiles_module).iterdir() if entry.is_dir()
    ]
    profile_details: list[ProfileDetails] = []
    for profile_file in profiles:
        profile_name = profile_file.name
        try:
            definition = profile_parser.parse_yaml_resource(
                package=".".join([profiles_module, profile_name]),
                resource="profile.yaml",
            )
            profile_details.append(
                ProfileDetails(name=profile_name, definition=definition)
            )
        except FileNotFoundError as e:
            print(f"WARN: profile.yaml not found for {profile_name}", e)
            continue
    return profile_details
