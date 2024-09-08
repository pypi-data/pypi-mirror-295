import logging

import fastapi


def register_api_router(app: fastapi.FastAPI):
    import inngest
    import inngest.fast_api

    inngest_client = inngest.Inngest(
        app_id="mtmai",
        logger=logging.getLogger("uvicorn"),
        env="dev",
        is_production=False,
        event_api_base_url="http://172.17.0.1:8288",
        api_base_url="http://172.17.0.1:8288",
        signing_key="signkey-prod-5446e845412cc5c77dc3338ff4e0a6d5e288b7327007921972d20fff9b989d60",
        event_key="rJwjHoCvDH2kIxLUvS2DlM85DSOSo7KVVr0Z4uhac7tg2h1a7Gw1kk8CslV3nzoBw2WQvVE37foClw26H6-LmA",
    )

    # Create an Inngest function
    @inngest_client.create_function(
        fn_id="mtai/hello",
        # Event that triggers this function
        trigger=inngest.TriggerEvent(event="mtai/hello"),
    )
    async def my_function(ctx: inngest.Context, step: inngest.Step) -> str:
        ctx.logger.info("hello run python -----------------------")
        ctx.logger.info(ctx.event)
        return "done"

    inngest.fast_api.serve(app, inngest_client, [my_function])
