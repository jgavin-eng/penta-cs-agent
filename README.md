# Penta CS Agent - Email Classification Agent

An intelligent email classification agent for Penta Fine Ingredients customer service routing. This agent uses advanced LLMs (Anthropic Claude or OpenAI GPT) to automatically classify incoming customer emails, extract relevant information, and route them to the appropriate department.

## Features

- **🤖 AI-Powered Classification**: Uses state-of-the-art LLMs (Anthropic Claude or OpenAI GPT-4) for accurate email classification
- **📚 Knowledge Base**: Vector-based knowledge base for storing product information and common queries
- **🔧 Function Calling**: Extensible tool system for calling external APIs and databases
- **📈 Learning System**: Feedback mechanism to improve classification accuracy over time
- **🎯 Multi-Category Support**: Supports 12+ email categories specific to chemical ingredients business
- **⚡ High Performance**: Fast classification with confidence scoring
- **🔒 Production Ready**: Comprehensive error handling and logging

## Email Categories

The agent can classify emails into the following categories:

- **Quote Request**: Customer requesting price quotes for products
- **Order Placement**: Customer placing a new order
- **Order Inquiry**: Questions about existing orders (status, tracking, etc.)
- **Product Inquiry**: Questions about product specifications, availability, or information
- **Technical Support**: Technical help with product application or formulation
- **Shipping Inquiry**: Questions about shipping options, costs, or delivery
- **Billing Inquiry**: Questions about invoices, payments, or account balance
- **Complaint**: Customer expressing dissatisfaction or reporting issues
- **Regulatory Compliance**: Questions about certifications, safety data sheets, or compliance
- **Sample Request**: Requests for product samples
- **General Inquiry**: General questions about the company or policies
- **Spam**: Unsolicited or irrelevant emails

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- API key for either Anthropic or OpenAI

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd penta-cs-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   # Choose your LLM provider
   LLM_PROVIDER=anthropic  # or 'openai'

   # Add your API key
   ANTHROPIC_API_KEY=your_key_here
   # OR
   OPENAI_API_KEY=your_key_here
   ```

4. **Optional: Set up knowledge base** (see examples/knowledge_base_setup.py):
   ```bash
   python examples/knowledge_base_setup.py
   ```

## Quick Start

### Basic Usage

```python
from src.penta_cs_agent import EmailClassificationAgent, EmailClassification

# Initialize the agent
agent = EmailClassificationAgent()

# Create an email to classify
email = EmailClassification(
    subject="Request for quote - Citric Acid",
    body="We need a price quote for 5000 kg of food-grade citric acid.",
    sender="customer@example.com"
)

# Classify the email
result = agent.classify(email)

print(f"Category: {result.primary_category.value}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Action: {result.recommended_action}")
```

### Advanced Usage with Custom Tools

```python
from src.penta_cs_agent import EmailClassificationAgent, AgentConfig
from src.penta_cs_agent.tools import ToolRegistry

# Create custom tool registry
registry = ToolRegistry()

@registry.register_decorator(
    name="lookup_customer",
    description="Look up customer information",
    parameters={
        "type": "object",
        "properties": {
            "email": {"type": "string"}
        },
        "required": ["email"]
    }
)
def lookup_customer(email: str):
    # Your custom logic here
    return {"customer_id": "123", "status": "premium"}

# Initialize agent with custom tools
agent = EmailClassificationAgent(tool_registry=registry)
```

### Learning from Feedback

```python
from src.penta_cs_agent import EmailCategory

# Classify an email
result = agent.classify(email)

# If the classification was wrong, provide feedback
agent.provide_feedback(
    email=email,
    original_classification=result.primary_category,
    correct_classification=EmailCategory.COMPLAINT,
    confidence=result.confidence,
    notes="Customer was actually complaining about billing error"
)
```

## Examples

The `examples/` directory contains comprehensive examples:

- **basic_usage.py**: Basic email classification examples
- **feedback_learning.py**: Demonstration of the learning system
- **custom_tools.py**: How to add custom tools and functions
- **knowledge_base_setup.py**: Populating the knowledge base with product data

Run any example:
```bash
python examples/basic_usage.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Email Input                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              EmailClassificationAgent                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLM Provider (Anthropic Claude / OpenAI GPT)        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Knowledge Base (ChromaDB Vector Store)              │  │
│  │  - Product Information                               │  │
│  │  - Common Queries                                    │  │
│  │  - Classification History                            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tool Registry (Function Calling)                    │  │
│  │  - Order Lookup                                      │  │
│  │  - Product Availability                              │  │
│  │  - Custom Tools                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Classification Result                           │
│  - Primary Category                                         │
│  - Confidence Score                                         │
│  - Extracted Entities                                       │
│  - Recommended Action                                       │
│  - Priority Level                                           │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

Configuration is managed through the `AgentConfig` class and environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (anthropic or openai) | anthropic |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_MODEL` | Anthropic model to use | claude-3-5-sonnet-20240620 |
| `OPENAI_MODEL` | OpenAI model to use | gpt-4-turbo-preview |
| `KNOWLEDGE_BASE_PATH` | Path to knowledge base | ./data/knowledge_base |
| `FEEDBACK_LOG_PATH` | Path to feedback log | ./data/feedback_log.json |
| `CONFIDENCE_THRESHOLD` | Minimum confidence threshold | 0.7 |
| `ENABLE_LEARNING` | Enable learning from feedback | true |

## API Reference

### EmailClassificationAgent

Main agent class for email classification.

**Methods:**

- `classify(email: EmailClassification) -> ClassificationResult`
  - Classify an email and return results

- `provide_feedback(email, original_classification, correct_classification, confidence, notes=None)`
  - Provide feedback for learning

- `get_statistics() -> Dict[str, Any]`
  - Get agent and knowledge base statistics

### EmailClassification

Input model for emails to classify.

**Fields:**
- `subject: str` - Email subject line
- `body: str` - Email body content
- `sender: Optional[str]` - Sender email address
- `received_at: Optional[datetime]` - When email was received
- `metadata: Optional[Dict]` - Additional metadata

### ClassificationResult

Output model for classification results.

**Fields:**
- `primary_category: EmailCategory` - Primary classification
- `confidence: float` - Confidence score (0-1)
- `secondary_categories: List[EmailCategory]` - Other possible categories
- `reasoning: str` - Explanation for classification
- `extracted_entities: Dict` - Extracted information
- `recommended_action: str` - Suggested next steps
- `priority: str` - Priority level (low, normal, high, urgent)

## Knowledge Base

The knowledge base uses ChromaDB for vector storage and similarity search. It stores:

1. **Product Information**: Product catalog with descriptions and metadata
2. **Common Queries**: Historical query patterns and their classifications
3. **Classification History**: Past email classifications for learning

### Populating the Knowledge Base

```python
from src.penta_cs_agent.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Add a product
kb.add_product(
    product_id="CA-001",
    name="Citric Acid",
    description="Food-grade citric acid...",
    category="Acidulants"
)

# Add a common query
kb.add_common_query(
    query_id="Q001",
    query_text="What is the price for bulk citric acid?",
    classification="quote_request",
    confidence=0.95
)
```

## Custom Tools

Extend the agent's capabilities by registering custom tools:

```python
from src.penta_cs_agent.tools import ToolRegistry

registry = ToolRegistry()

@registry.register_decorator(
    name="your_tool_name",
    description="What your tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Description"}
        },
        "required": ["param1"]
    }
)
def your_custom_function(param1: str):
    # Your implementation
    return {"result": "data"}
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Production Deployment

For production deployment:

1. **Set up proper API key management** (use secrets manager)
2. **Configure persistent storage** for knowledge base
3. **Set up monitoring** for classification accuracy
4. **Implement rate limiting** for API calls
5. **Add error tracking** (e.g., Sentry)
6. **Regular feedback review** to improve accuracy
7. **Backup knowledge base** regularly

## Performance

- Average classification time: 1-3 seconds (depending on LLM provider and model)
- Confidence threshold: 70% (configurable)
- Supports concurrent processing
- Knowledge base search: <100ms

## Limitations

- Requires internet connection for LLM API calls
- Classification quality depends on LLM model chosen
- Initial setup requires API keys for Anthropic or OpenAI
- Knowledge base grows over time (plan for storage)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- Create an issue in the repository
- Contact: [your-email@penta.com]

## Changelog

### Version 1.0.0
- Initial release
- Support for Anthropic Claude and OpenAI GPT
- Vector-based knowledge base
- Function calling framework
- Learning system with feedback
- 12 email categories
- Comprehensive examples and documentation
