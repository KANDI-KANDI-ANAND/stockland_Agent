class ContextService:

    @staticmethod
    def build_context(results):

        context_parts = []

        for r in results:

            title = r.get("title", "")
            summary = r.get("summary", "")

            context_parts.append(
                f"{title}\n{summary}"
            )

        context = "\n\n".join(context_parts)

        return context