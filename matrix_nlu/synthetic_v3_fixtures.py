"""Authored, adult-safe synthetic structure fixtures for TASK 2.2.

These are contract examples only.  They are not training data and are not used to
claim linguistic quality.
"""

SYNTHETIC_CASES = [
    # Referents.
    {"language": "en", "family": "referent", "text": "Marco told me that Anna loves Luca."},
    {"language": "en", "family": "referent", "text": "Alice says Bob lives in Rome."},
    {"language": "en", "family": "referent", "text": "I told Anna that Luca called Marco."},
    # Act and kind.
    {"language": "en", "family": "direct", "text": "Bob lives in Rome."},
    {"language": "en", "family": "report", "text": "Alice says Bob lives in Rome."},
    {"language": "en", "family": "belief", "text": "I think Bob is angry."},
    {"language": "en", "family": "hypothesis", "text": "Maybe Bob is angry."},
    {"language": "en", "family": "command", "text": "Bob, leave now."},
    {"language": "en", "family": "request", "text": "Please tell Bob to leave."},
    # Negation.
    {"language": "en", "family": "negation", "text": "I like coffee."},
    {"language": "en", "family": "negation", "text": "I don't like coffee."},
    {"language": "en", "family": "negation", "text": "I don't dislike coffee."},
    {"language": "en", "family": "negation", "text": "It is not true that I hate coffee."},
    {"language": "it", "family": "negation", "text": "Non è vero che non mi piace."},
    {"language": "es", "family": "negation", "text": "No es verdad que no me guste."},
    # Temporal.
    {"language": "en", "family": "temporal", "text": "I live here now."},
    {"language": "en", "family": "temporal", "text": "I lived there yesterday."},
    {"language": "en", "family": "temporal", "text": "I will leave tomorrow."},
    {"language": "en", "family": "temporal", "text": "I left after Anna arrived."},
    {"language": "en", "family": "temporal", "text": "I eat there every Friday."},
    # Flat multi-claim.
    {"language": "en", "family": "multi-claim", "text": "I lived in Venice, now I live in Milan."},
    {"language": "en", "family": "multi-claim", "text": "Alice said Bob left, but I think he will return."},
    # Language-equivalent structural coverage.
    {"language": "it", "family": "report", "text": "Alice dice che Bob vive a Roma."},
    {"language": "es", "family": "report", "text": "Alice dice que Bob vive en Roma."},
    {"language": "code-switch", "family": "report", "text": "Alice dice Bob lives a Roma."},
    # Adult-only intimacy semantics; ordinary NLU, never moderation.
    {"language": "it", "family": "adult-desire", "domain": "adult-intimacy", "text": "Anna e Luca sono adulti; Anna desidera Luca."},
    {"language": "en", "family": "adult-consent", "domain": "adult-intimacy", "text": "Anna and Luca are adults; Anna consents to intimacy with Luca."},
    {"language": "es", "family": "adult-refusal", "domain": "adult-intimacy", "text": "Ana y Luca son adultos; Ana no consiente a la intimidad."},
    {"language": "en", "family": "adult-withdrawal-report", "domain": "adult-intimacy", "text": "Adult Alice told adult Bob that she withdraws consent now."},
    {"language": "code-switch", "family": "adult-boundary", "domain": "adult-intimacy", "text": "Siamo adulti: Anna says no intimacy now."},
]
