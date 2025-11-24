# Anti-Detection Strategy for GPTZero

## Understanding GPTZero Detection

GPTZero uses two primary metrics to detect AI-generated content:

### 1. Perplexity (Text Predictability)
- **AI Text**: LOW perplexity - very predictable word choices
- **Human Text**: HIGH perplexity - unexpected, varied word choices
- **Goal**: Increase perplexity by using unexpected phrasing and vocabulary

### 2. Burstiness (Sentence Variation)
- **AI Text**: LOW burstiness - uniform sentence lengths and structures
- **Human Text**: HIGH burstiness - highly varied sentence patterns
- **Goal**: Mix short, medium, and long sentences with diverse structures

### 3. Additional Red Flags
- Uniform predictability
- Repetitive phrasing patterns
- Consistent paragraph lengths
- Lack of vocabulary diversity
- Perfect grammar (humans make minor errors)
- Over-formal tone

## Implementation Strategy

### Phase 1: Enhanced Training Data (Critical!)
**Current State**: Only 2 examples in database
**Target**: Minimum 50-100 diverse examples per content type

#### Required Content Types:
1. **Sales/Marketing** (30+ examples)
   - Email campaigns
   - Product descriptions
   - Landing page copy
   - Social media ads
   - Sales letters

2. **Journalism** (30+ examples)
   - News articles
   - Opinion pieces
   - Feature stories
   - Blog posts
   - Investigative reports

#### Key Characteristics to Include:
- Varied sentence lengths (5-50 words)
- Natural errors/typos (occasional)
- Colloquialisms and slang
- Informal contractions
- Personal anecdotes
- Emotional language
- Unexpected word choices
- Fragment sentences (when appropriate)
- Run-on sentences (occasional)

### Phase 2: Improved Agent Prompts

#### Style Transformer Enhancements:
- **Increase Perplexity**: Use unexpected synonyms, varied vocabulary
- **Increase Burstiness**: Mix sentence lengths dramatically
- **Add Imperfections**: Minor grammar variations, natural flow breaks
- **Vary Paragraph Length**: 1-5 sentences, not uniform
- **Use Natural Voice**: Contractions, fragments, emphasis

#### Quality Checker Enhancements:
- Measure perplexity score
- Measure burstiness score
- Check vocabulary diversity (TTR - Type-Token Ratio)
- Verify sentence length variance
- Detect AI patterns (transitions, formal phrases)

### Phase 3: Advanced Humanization Techniques

1. **Sentence Length Variance**
   - Target: Standard deviation > 10 words
   - Mix: 3-word fragments with 40-word complex sentences

2. **Vocabulary Diversity**
   - Avoid repetitive words
   - Use synonyms naturally
   - Include domain-specific jargon appropriately

3. **Natural Imperfections**
   - Strategic comma splices (rare)
   - Sentence fragments for emphasis
   - Occasional contractions in formal text
   - Natural flow interruptions

4. **Emotional Authenticity**
   - Personal touches
   - Genuine enthusiasm or concern
   - Subjective opinions
   - Relatable examples

5. **Structural Variation**
   - Vary paragraph opening styles
   - Mix simple and complex sentences
   - Use questions, exclamations
   - Break expected patterns

## Success Metrics

- **Perplexity Score**: > 100 (higher = more human)
- **Burstiness Score**: > 0.5 (higher = more human)
- **Lexical Diversity**: > 0.7 (TTR ratio)
- **Sentence Length Std Dev**: > 10 words
- **GPTZero Detection**: < 20% AI probability

## Next Steps

1. ✅ Research completed
2. ⏳ Enhance agent prompts
3. ⏳ Collect 100+ human-written examples
4. ⏳ Implement advanced metrics
5. ⏳ Test against GPTZero
6. ⏳ Iterate based on results
