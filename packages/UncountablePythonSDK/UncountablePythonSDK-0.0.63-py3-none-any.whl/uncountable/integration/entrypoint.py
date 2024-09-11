from uncountable.integration.db.connect import create_db_engine
from uncountable.integration.scan_profiles import load_profiles
from uncountable.integration.server import IntegrationServer


def main(blocking: bool) -> None:
    with IntegrationServer(create_db_engine()) as server:
        for profile_details in load_profiles():
            server.register_profile(
                profile_name=profile_details.name,
                base_url=profile_details.definition.base_url,
                auth_retrieval=profile_details.definition.auth_retrieval,
                jobs=profile_details.definition.jobs,
                client_options=profile_details.definition.client_options,
            )

        if blocking:
            server.serve_forever()


main(__name__ == "__main__")
