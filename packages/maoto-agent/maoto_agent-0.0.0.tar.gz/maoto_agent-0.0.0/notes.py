# TODO s:

# TODO: J.A.V.I.S. – "Joint Artificial Virtual Intelligence System"

# TODO: associate actions with responses using responses_actions table and check for actioncalls if they follow up on a response that has the action attached
# TODO: enable overwriting an actioncall (when same name)
# TODO: encryption

# TODO: publish first version of packages

# TODO: authentification: enable resolver account disconnection (provide attached accounts list in llm context)
# TODO: proper error handling for llm when maoto call fails
# TODO: create options for user to detele subscriptions (provide current subscriptions in llm context)
# TODO: only send late reponses and actioncalls, when post stil open or still subscribed to apikey
# # Test updateSubscriptions table
# try:
#     maoto_provider.update_subscription([maoto_resolver.get_api_key()])
#     print("Subscription updated with new API keys.")
#     maoto_resolver.update_subscription([maoto_provider.get_api_key()])
#     print("Subscription updated with new API keys.\n")
# except Exception as e:
#     print(f"Failed to update subscription: {e}\n")


# TODO: switch psycopg2 to asyncpg
# TODO: make client requests async as well
# TODO: use context in posts and actioncalls

# TODO: notifications of user (cal)
# TODO: automatoc reconnection with backoff, if connection fails

# TODO: ingress with SSL certificate from Let's Encrypt and route different domains to different services (api, UI)
# TODO: add query validators: https://ariadnegraphql.org/docs/query-validators
# TODO: Implement query complexity analysis to prevent expensive queries that can lead to Denial of Service (DoS) attacks.
# TODO: Ariadne supports depth limiting
# TODO: Rate Limiting You can use libraries like starlette-limiter
# TODO: Error Handling: Ensure proper error handling to avoid exposing internal implementation details: ServerErrorMiddleware