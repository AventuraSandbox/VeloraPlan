from dotenv import load_dotenv
load_dotenv()

#!/usr/bin/env python3
"""
Test script to verify OpenAI GPT-3.5 integration and cost optimization
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_openai_setup():
    """Test if OpenAI can be configured with cost optimization"""
    try:
        from crewai.llm import LLM
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY environment variable not set")
            print("💡 Please set your OpenAI API key: export OPENAI_API_KEY='your-api-key'")
            return False
        
        print("✅ OpenAI API key found")
        
        # Test with cost-optimized configuration
        llm = LLM(
            provider="openai",
            model="gpt-4.1-nano",
            api_key=api_key,
            temperature=0.1,
            max_tokens=1000,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        print("✅ OpenAI LLM object created successfully!")
        print("🤖 Model: gpt-4.1-nano (Cost Optimized)")
        print("💰 Cost-saving features: temperature=0.1, max_tokens=1000")
        
        # Test a simple prompt
        try:
            result = llm.call("What is project management? Keep response under 100 words.")
            print(f"✅ Test response: {result[:100]}...")
            
            # Estimate cost for this test
            estimated_cost = len(result.split()) * 0.0015 / 1000  # Rough estimate
            print(f"💰 Estimated cost for this test: ~${estimated_cost:.4f}")
            
            return True
        except Exception as e:
            print(f"⚠️  API call failed: {e}")
            print("💡 This might be due to insufficient credits or API issues")
            return False
        
    except Exception as e:
        print(f"❌ OpenAI setup failed: {e}")
        return False

def test_cost_estimation():
    """Test the cost estimation functionality"""
    try:
        from veloraplan.crew import Veloraplan, cost_estimator
        
        print("\n🧮 Testing cost estimation...")
        
        # Create a test instance
        veloraplan = Veloraplan()
        
        # Simulate some token usage
        cost_estimator.add_usage(2000, 1000)  # 2K input, 1K output tokens
        
        # Get cost estimate
        estimate = veloraplan.get_cost_estimate()
        print(f"✅ Cost estimation working:")
        print(f"   Input tokens: {estimate['input_tokens']:,}")
        print(f"   Output tokens: {estimate['output_tokens']:,}")
        print(f"   Estimated cost: ${estimate['estimated_cost_usd']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cost estimation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing OpenAI GPT-3.5 Integration (Cost Optimized)")
    print("=" * 60)
    
    # Test basic setup
    setup_success = test_openai_setup()
    
    # Test cost estimation
    cost_success = test_cost_estimation()
    
    print("\n" + "=" * 60)
    if setup_success and cost_success:
        print("✅ All tests passed! OpenAI integration is ready.")
        print("💰 Cost optimization features are active.")
        print("💡 Expected cost per run: $0.01-0.05")
    else:
        print("❌ Some tests failed. Please check the error messages above.") 