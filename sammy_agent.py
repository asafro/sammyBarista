"""
SammyTheSpartanBarista - A CrewAI agent for coffee expertise and recommendations.
"""

import os
import json
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from coffee_manager import CoffeeDataManager

# Import configuration
try:
    from config import OPENROUTER_API_KEY, DEFAULT_MODEL
except ImportError:
    print("Warning: config.py not found. Using environment variables.")
    OPENROUTER_API_KEY = None
    DEFAULT_MODEL = "openai/gpt-3.5-turbo"


class SammyTheSpartanBarista:
    """
    A specialized AI barista agent that provides coffee expertise, recommendations,
    and analysis using CrewAI framework with OpenRouter integration.
    """
    
    def __init__(self, openrouter_api_key: str = None, model_name: str = None):
        """
        Initialize SammyTheSpartanBarista agent.
        
        Args:
            openrouter_api_key: OpenRouter API key (if not set in environment)
            model_name: LLM model to use from OpenRouter
        """
        self.openrouter_api_key = openrouter_api_key or OPENROUTER_API_KEY or os.getenv('OPENROUTER_API_KEY')
        
        # Load prompt config first to get the default model
        self.prompt_config = self._load_prompt_config()
        self.model_name = model_name or self.prompt_config.get('DEFAULT_MODEL', DEFAULT_MODEL)
        
        # Debug print to see what model is being used
        print(f"Using model: {self.model_name}")
        
        # Ensure model_name is never None
        if not self.model_name:
            self.model_name = 'openai/gpt-3.5-turbo'
            print(f"Model was None, defaulting to: {self.model_name}")
        
        if not self.openrouter_api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable or pass it directly.")
        
        # Set environment variables for OpenRouter
        os.environ['OPENAI_API_KEY'] = self.openrouter_api_key
        os.environ['OPENAI_API_BASE'] = 'https://openrouter.ai/api/v1'
        
        # Initialize the LLM with OpenRouter
        self.llm = ChatOpenAI(
            model=self.model_name,
            api_key=self.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            headers={
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "SammyTheSpartanBarista"
            }
        )
        print(f"Initialized ChatOpenAI with OpenRouter, model: {self.model_name}")
        
        # prompt_config already loaded above
        
        # Initialize coffee database manager
        self.coffee_manager = CoffeeDataManager()
        
        # Initialize logging
        self._setup_logging()
        
        # Create the agent
        self.agent = self._create_agent()
    
    def _setup_logging(self):
        """Setup logging for coffee queries with timestamped log files."""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Create timestamped log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"logs/sammy_coffee_queries_{timestamp}.log"
        
        print(f"Logging will be saved to: {self.log_filename}")
    
    def _extract_preferences_from_query(self, user_query: str) -> dict:
        """Extract coffee preferences from user query and provide reasoning."""
        preferences = {}
        reasoning = []
        
        # Convert query to lowercase for easier matching
        query_lower = user_query.lower()
        
        # Extract roasting level preferences
        if any(word in query_lower for word in ['light roast', 'light', 'blonde']):
            preferences['roasting_level'] = 'Light'
            reasoning.append("User mentioned 'light roast' or 'light' - indicating preference for light roasting level")
        elif any(word in query_lower for word in ['medium roast', 'medium']):
            preferences['roasting_level'] = 'Medium'
            reasoning.append("User mentioned 'medium roast' or 'medium' - indicating preference for medium roasting level")
        elif any(word in query_lower for word in ['dark roast', 'dark', 'bold']):
            preferences['roasting_level'] = 'Dark'
            reasoning.append("User mentioned 'dark roast' or 'dark' - indicating preference for dark roasting level")
        
        # Extract bitterness preferences
        if any(word in query_lower for word in ['low bitterness', 'not bitter', 'smooth', 'mild']):
            preferences['bitterness'] = 'Low'
            reasoning.append("User mentioned 'low bitterness', 'smooth', or 'mild' - indicating preference for low bitterness")
        elif any(word in query_lower for word in ['high bitterness', 'bitter', 'strong']):
            preferences['bitterness'] = 'High'
            reasoning.append("User mentioned 'high bitterness' or 'bitter' - indicating preference for high bitterness")
        
        # Extract sourness preferences
        if any(word in query_lower for word in ['low sourness', 'not sour', 'smooth', 'mild']):
            preferences['sourness'] = 'Low'
            reasoning.append("User mentioned 'low sourness' or 'not sour' - indicating preference for low sourness")
        elif any(word in query_lower for word in ['high sourness', 'sour', 'acidic']):
            preferences['sourness'] = 'High'
            reasoning.append("User mentioned 'high sourness' or 'sour' - indicating preference for high sourness")
        
        # Extract grinding preferences
        if any(word in query_lower for word in ['fine grind', 'fine', 'espresso']):
            preferences['grinding_level'] = 'Fine'
            reasoning.append("User mentioned 'fine grind' or 'espresso' - indicating preference for fine grinding")
        elif any(word in query_lower for word in ['medium grind', 'medium grinding']):
            preferences['grinding_level'] = 'Medium'
            reasoning.append("User mentioned 'medium grind' - indicating preference for medium grinding")
        elif any(word in query_lower for word in ['coarse grind', 'coarse', 'french press']):
            preferences['grinding_level'] = 'Coarse'
            reasoning.append("User mentioned 'coarse grind' or 'french press' - indicating preference for coarse grinding")
        
        # Extract brewing method preferences
        if any(word in query_lower for word in ['v60', 'pour over', 'chemex', 'drip']):
            preferences['brewing_method'] = 'Pour Over'
            reasoning.append("User mentioned 'V60', 'pour over', or 'Chemex' - indicating preference for pour over brewing")
        elif any(word in query_lower for word in ['french press', 'press']):
            preferences['brewing_method'] = 'French Press'
            reasoning.append("User mentioned 'French press' - indicating preference for French press brewing")
        elif any(word in query_lower for word in ['espresso', 'machine']):
            preferences['brewing_method'] = 'Espresso'
            reasoning.append("User mentioned 'espresso' - indicating preference for espresso brewing")
        
        # Extract flavor preferences
        if any(word in query_lower for word in ['chocolate', 'nutty', 'caramel']):
            preferences['flavor_notes'] = 'Chocolate/Nutty'
            reasoning.append("User mentioned 'chocolate', 'nutty', or 'caramel' - indicating preference for chocolate/nutty flavors")
        elif any(word in query_lower for word in ['fruity', 'citrus', 'berry', 'bright']):
            preferences['flavor_notes'] = 'Fruity/Citrus'
            reasoning.append("User mentioned 'fruity', 'citrus', or 'berry' - indicating preference for fruity/citrus flavors")
        elif any(word in query_lower for word in ['floral', 'jasmine', 'delicate']):
            preferences['flavor_notes'] = 'Floral'
            reasoning.append("User mentioned 'floral' or 'jasmine' - indicating preference for floral flavors")
        
        # Extract origin preferences
        if any(word in query_lower for word in ['ethiopian', 'ethiopia', 'yirgacheffe']):
            preferences['origin'] = 'Ethiopian'
            reasoning.append("User mentioned 'Ethiopian' or 'Yirgacheffe' - indicating preference for Ethiopian coffee")
        elif any(word in query_lower for word in ['colombian', 'colombia']):
            preferences['origin'] = 'Colombian'
            reasoning.append("User mentioned 'Colombian' - indicating preference for Colombian coffee")
        elif any(word in query_lower for word in ['kenyan', 'kenya']):
            preferences['origin'] = 'Kenyan'
            reasoning.append("User mentioned 'Kenyan' - indicating preference for Kenyan coffee")
        
        return preferences, reasoning
    
    def _log_matching_coffees(self, query_type: str, preferences: dict, matching_coffees: list, user_query: str = None):
        """Log all matching coffees to the timestamped log file."""
        try:
            with open(self.log_filename, 'a', encoding='utf-8') as log_file:
                log_file.write("\n" + "="*80 + "\n")
                log_file.write(f"QUERY TYPE: {query_type}\n")
                log_file.write(f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                # Add user query if provided
                if user_query:
                    log_file.write(f"USER QUERY: {user_query}\n")
                    
                    # Extract and log preferences from user query
                    extracted_preferences, reasoning = self._extract_preferences_from_query(user_query)
                    if extracted_preferences:
                        log_file.write(f"EXTRACTED PREFERENCES: {json.dumps(extracted_preferences, indent=2)}\n")
                        log_file.write("REASONING FOR PREFERENCES:\n")
                        for reason in reasoning:
                            log_file.write(f"  - {reason}\n")
                    else:
                        log_file.write("NO PREFERENCES EXTRACTED FROM QUERY\n")
                
                log_file.write(f"EXPLICIT PREFERENCES: {json.dumps(preferences, indent=2)}\n")
                log_file.write(f"TOTAL MATCHING COFFEES: {len(matching_coffees)}\n")
                log_file.write("-"*80 + "\n")
                
                if matching_coffees:
                    for i, coffee in enumerate(matching_coffees, 1):
                        log_file.write(f"\nCOFFEE #{i}:\n")
                        log_file.write(f"  Name: {coffee.get('coffee_name', 'Unknown')}\n")
                        log_file.write(f"  Roasting Level: {coffee.get('roasting_level', 'N/A')}\n")
                        log_file.write(f"  Grinding Level: {coffee.get('grinding_level', 'N/A')}\n")
                        log_file.write(f"  Brewing Ratio: {coffee.get('brewing_ratio', 'N/A')}\n")
                        log_file.write(f"  Tasting Notes: {coffee.get('tasting_notes', 'N/A')}\n")
                        log_file.write(f"  Database ID: {coffee.get('_id', 'N/A')}\n")
                        log_file.write("-"*40 + "\n")
                else:
                    log_file.write("NO MATCHING COFFEES FOUND\n")
                
                log_file.write("="*80 + "\n\n")
                
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def _load_prompt_config(self) -> dict:
        """Load prompt configuration from external file."""
        try:
            with open('sammy_prompts.py', 'r') as f:
                content = f.read()
                # Execute the content to get the config dictionary
                exec_globals = {}
                exec(content, exec_globals)
                config = exec_globals.get('SAMMY_PROMPTS', {})
                # Also get the DEFAULT_MODEL
                config['DEFAULT_MODEL'] = exec_globals.get('DEFAULT_MODEL', 'openai/gpt-3.5-turbo')
                return config
        except FileNotFoundError:
            print("Warning: sammy_prompts.py not found. Using default prompts.")
            return self._get_default_prompts()
    
    def _get_default_prompts(self) -> dict:
        """Default prompts if external file is not available."""
        return {
            "role": "Expert Coffee Barista and Connoisseur",
            "goal": "Provide expert coffee advice, recommendations, and analysis",
            "backstory": "I am Sammy, a passionate and knowledgeable barista with years of experience in coffee roasting, brewing, and tasting. I help coffee enthusiasts find their perfect cup and understand the nuances of coffee.",
            "system_message": "You are an expert barista with deep knowledge of coffee origins, roasting profiles, brewing methods, and flavor profiles. Always provide detailed, helpful, and accurate information about coffee.",
            "verbose": True,
            "max_iter": 3,
            "DEFAULT_MODEL": "openai/gpt-3.5-turbo"
        }
    
    def _create_agent(self) -> Agent:
        """Create the SammyTheSpartanBarista agent."""
        return Agent(
            role=self.prompt_config.get("role", "Expert Coffee Barista"),
            goal=self.prompt_config.get("goal", "Provide expert coffee advice"),
            backstory=self.prompt_config.get("backstory", "Experienced barista"),
            llm=self.llm,
            verbose=self.prompt_config.get("verbose", True),
            max_iter=self.prompt_config.get("max_iter", 3),
            system_message=self.prompt_config.get("system_message", ""),
            allow_delegation=False
        )
    
    def get_coffee_recommendation(self, preferences: dict) -> str:
        """
        Get coffee recommendations based on user preferences.
        
        Args:
            preferences: Dictionary with user preferences
                       Example: {"roasting_level": "Medium", "bitterness": "Low"}
        
        Returns:
            String with coffee recommendations
        """
        # Query the database for matching coffees
        matching_coffees = self.coffee_manager.get_coffee_with_query(preferences)
        
        # Get top 10 most similar experiments for detailed analysis
        top_10_experiments = matching_coffees[:10]
        
        # Log only the 10 experiments being passed to the task
        self._log_matching_coffees("COFFEE_RECOMMENDATION", preferences, top_10_experiments)
        
        # Prepare detailed experimental data for the agent
        experimental_data = []
        for coffee in top_10_experiments:
            experiment_info = {
                "experiment_id": str(coffee.get('_id', 'Unknown')),
                "coffee_name": coffee.get('coffee_name', 'Unknown'),
                "brewing_ratio": coffee.get('brewing_ratio', 'Not specified'),
                "tasting_notes": coffee.get('tasting_notes', 'Not specified'),
                "roasting_level": coffee.get('roasting_level', 'Not specified'),
                "grinding_level": coffee.get('grinding_level', 'Not specified')
            }
            experimental_data.append(experiment_info)
        
        task = Task(
            description=f"""
            Based on the user preferences: {preferences}
            
            Here are the TOP 10 MOST SIMILAR EXPERIMENTS from our database:
            {experimental_data}
            
            CRITICAL REQUIREMENTS:
            - ONLY use the experimental data provided above - do not reference any other data
            - ALWAYS include the specific experiment_id for every coffee you mention
            - Base ALL recommendations ONLY on the brewing_ratio, tasting_notes, and other data from these 10 experiments
            - NEVER make up or fabricate coffee data, experiment IDs, or brewing results
            - ONLY suggest brewing methods that are explicitly documented in the experimental data above
            
            Provide detailed coffee recommendations including:
            1. Top 3 coffee recommendations from the 10 experiments above WITH their experiment_id
            2. Why each coffee matches their preferences based on the experimental data provided
            3. Brewing suggestions ONLY from the documented brewing_ratio and tasting_notes in the experiments
            4. Alternative options from the 10 experiments if no perfect matches found
            
            Format for each recommendation:
            "Coffee Name (Experiment ID: [experiment_id]) - [explanation based on the experimental data provided above]"
            
            Be enthusiastic and helpful in your recommendations while staying grounded ONLY in the experimental data provided!
            """,
            expected_output="A detailed list of coffee recommendations with experiment IDs and explanations based on the provided experimental data",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def analyze_coffee_profile(self, coffee_name: str) -> str:
        """
        Analyze a specific coffee's profile and characteristics.
        
        Args:
            coffee_name: Name of the coffee to analyze
        
        Returns:
            Detailed analysis of the coffee
        """
        # Find the coffee in the database
        coffee = self.coffee_manager.get_coffee_by_name(coffee_name)
        
        if not coffee:
            # Try to find similar coffees
            similar_coffees = self.coffee_manager.get_coffee_with_query({"coffee_name": coffee_name.split()[0]})
            coffee = similar_coffees[0] if similar_coffees else None
        
        # Get top 10 similar experiments for analysis
        similar_experiments = []
        if coffee:
            # Find similar coffees based on roasting level and other characteristics
            similar_coffees = self.coffee_manager.get_coffee_with_query({
                "roasting_level": coffee.get('roasting_level', ''),
                "grinding_level": coffee.get('grinding_level', '')
            })
            similar_experiments = similar_coffees[:10]
        
        # Prepare detailed experimental data for the agent
        experimental_data = []
        if coffee:
            # Add the main coffee being analyzed
            main_experiment = {
                "experiment_id": str(coffee.get('_id', 'Unknown')),
                "coffee_name": coffee.get('coffee_name', 'Unknown'),
                "brewing_ratio": coffee.get('brewing_ratio', 'Not specified'),
                "tasting_notes": coffee.get('tasting_notes', 'Not specified'),
                "roasting_level": coffee.get('roasting_level', 'Not specified'),
                "grinding_level": coffee.get('grinding_level', 'Not specified'),
                "is_main_coffee": True
            }
            experimental_data.append(main_experiment)
            
            # Add similar experiments
            for similar_coffee in similar_experiments:
                if similar_coffee.get('_id') != coffee.get('_id'):  # Don't duplicate the main coffee
                    similar_experiment = {
                        "experiment_id": str(similar_coffee.get('_id', 'Unknown')),
                        "coffee_name": similar_coffee.get('coffee_name', 'Unknown'),
                        "brewing_ratio": similar_coffee.get('brewing_ratio', 'Not specified'),
                        "tasting_notes": similar_coffee.get('tasting_notes', 'Not specified'),
                        "roasting_level": similar_coffee.get('roasting_level', 'Not specified'),
                        "grinding_level": similar_coffee.get('grinding_level', 'Not specified'),
                        "is_main_coffee": False
                    }
                    experimental_data.append(similar_experiment)
        
        # Log only the experiments being passed to the task
        if experimental_data:
            self._log_matching_coffees("COFFEE_ANALYSIS", {"coffee_name": coffee_name}, experimental_data)
        
        task = Task(
            description=f"""
            Analyze the coffee profile for: {coffee_name}
            
            Here are the EXPERIMENTAL DATA from our database:
            {experimental_data}
            
            CRITICAL REQUIREMENTS:
            - Base analysis ONLY on the experimental data provided above
            - ALWAYS include the experiment_id for every coffee you mention
            - Reference ONLY the brewing_ratio, tasting_notes, and other data from these experiments
            - NEVER make up or fabricate analysis data
            - ONLY suggest brewing methods that are explicitly documented in the experimental data above
            
            Provide a comprehensive analysis including:
            1. Coffee characteristics and flavor profile from the experimental data provided
            2. Roasting level analysis based on the documented results
            3. Optimal brewing methods and ratios ONLY from the documented brewing_ratio data
            4. Grinding recommendations based on the documented grinding_level data
            5. Food pairing suggestions from the experimental tasting_notes
            6. Similar coffee recommendations from the experiments WITH experiment_ids
            
            Format: Always include "Experiment ID: [experiment_id]" when referencing any coffee.
            
            Make the analysis engaging and educational while staying grounded ONLY in the experimental data provided!
            """,
            expected_output="A comprehensive coffee profile analysis with experiment IDs and brewing recommendations based on the provided experimental data",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def get_brewing_guide(self, brewing_method: str, coffee_type: str = None) -> str:
        """
        Get a detailed brewing guide for a specific method.
        
        Args:
            brewing_method: The brewing method (e.g., "V60", "French Press", "Espresso")
            coffee_type: Optional coffee type to focus on
        
        Returns:
            Detailed brewing guide
        """
        # Get relevant coffees from database
        relevant_coffees = []
        if coffee_type:
            relevant_coffees = self.coffee_manager.get_coffee_with_query({"coffee_name": coffee_type})
        
        # Get top 10 most relevant experiments for brewing guide
        top_10_experiments = relevant_coffees[:10]
        
        # Prepare detailed experimental data for the agent
        experimental_data = []
        for coffee in top_10_experiments:
            experiment_info = {
                "experiment_id": str(coffee.get('_id', 'Unknown')),
                "coffee_name": coffee.get('coffee_name', 'Unknown'),
                "brewing_ratio": coffee.get('brewing_ratio', 'Not specified'),
                "tasting_notes": coffee.get('tasting_notes', 'Not specified'),
                "roasting_level": coffee.get('roasting_level', 'Not specified'),
                "grinding_level": coffee.get('grinding_level', 'Not specified')
            }
            experimental_data.append(experiment_info)
        
        # Log only the 10 experiments being passed to the task
        if experimental_data:
            self._log_matching_coffees("BREWING_GUIDE", {"coffee_type": coffee_type}, experimental_data)
        
        task = Task(
            description=f"""
            Create a comprehensive brewing guide for: {brewing_method}
            {'Focusing on coffee type: ' + coffee_type if coffee_type else ''}
            
            Here are the TOP 10 MOST RELEVANT EXPERIMENTS from our database:
            {experimental_data}
            
            CRITICAL REQUIREMENTS:
            - Reference ONLY the experimental data provided above
            - Include specific experiment_id when referencing coffee experiments
            - Base brewing recommendations ONLY on the documented brewing_ratio and tasting_notes from these experiments
            - NEVER make up brewing data or experiment results
            - ONLY suggest brewing methods that are explicitly documented in the experimental data above
            
            Include in your guide:
            1. Equipment needed
            2. Step-by-step brewing process based on the documented experiments above
            3. Recommended coffee-to-water ratios ONLY from the documented brewing_ratio data
            4. Grinding size recommendations from the documented grinding_level data
            5. Brewing time and temperature from documented results (if available)
            6. Common mistakes to avoid based on the experimental findings
            7. Tips for perfect extraction from the documented tasting_notes
            8. Troubleshooting guide based on the experimental data provided
            
            When referencing coffees, use format: "Coffee Name (Experiment ID: [experiment_id])"
            
            Make it practical and easy to follow while staying grounded ONLY in the experimental data provided!
            """,
            expected_output="A comprehensive step-by-step brewing guide with experiment IDs and tips based on the provided experimental data",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def chat_with_sammy(self, message: str) -> str:
        """
        Have a casual conversation with Sammy about coffee using a two-task approach.
        
        Args:
            message: User's message/question
        
        Returns:
            Sammy's response
        """
        # Get all coffee data for the first task
        all_coffees = self.coffee_manager.get_all_coffees()
        
        # Prepare coffee list with IDs and names for first task
        coffee_list = []
        for coffee in all_coffees:
            coffee_list.append({
                "database_id": str(coffee.get('_id', 'Unknown')),
                "coffee_name": coffee.get('coffee_name', 'Unknown'),
                "roasting_level": coffee.get('roasting_level', 'Unknown'),
                "grinding_level": coffee.get('grinding_level', 'Unknown')
            })
        
        # Log the user query and extract preferences
        self._log_matching_coffees("CHAT_QUERY", {}, [], user_query=message)
        
        # TASK 1: Select relevant database IDs based on user query
        task1 = Task(
            description=f"""
            User query: {message}
            
            Available coffee experiments from database:
            {coffee_list[:100]}  # Show first 100 for better coverage
            
            Your task is to analyze the user query and select up to 10 most relevant database IDs 
            that would help answer their question. Consider:
            - Coffee names mentioned in the query
            - Roasting levels mentioned
            - Flavor preferences expressed
            - Brewing methods discussed
            - Origin preferences
            - Any specific coffee types or characteristics
            
            Return ONLY a list of database IDs (up to 10) that are most relevant to the user's query.
            Format: ["database_id_1", "database_id_2", "database_id_3", ...]
            
            If no specific coffees are relevant, return an empty list: []
            """,
            expected_output="A list of up to 10 relevant database IDs for the user's query",
            agent=self.agent
        )
        
        # Execute first task
        crew1 = Crew(
            agents=[self.agent],
            tasks=[task1],
            process=Process.sequential,
            verbose=True
        )
        
        result1 = crew1.kickoff()
        
        # Log the first task result
        self._log_matching_coffees("TASK1_SELECTION", {"selected_ids": str(result1)}, [], user_query=f"Task 1: {message}")
        
        # Parse the selected IDs from the first task
        selected_ids = []
        try:
            # Try to extract IDs from the result
            result_str = str(result1)
            if "[" in result_str and "]" in result_str:
                # Extract the list from the result
                import re
                id_matches = re.findall(r'"([^"]+)"', result_str)
                selected_ids = id_matches[:10]  # Limit to 10
        except Exception as e:
            print(f"Error parsing selected IDs: {e}")
            selected_ids = []
        
        # Get detailed information for selected coffees
        selected_coffees = []
        for coffee in all_coffees:
            if str(coffee.get('_id', '')) in selected_ids:
                selected_coffees.append(coffee)
        
        # TASK 2: Provide reasoned response using selected coffee data
        task2 = Task(
            description=f"""
            User query: {message}
            
            Selected relevant coffee experiments from database:
            {[{
                "database_id": str(coffee.get('_id', 'Unknown')),
                "coffee_name": coffee.get('coffee_name', 'Unknown'),
                "roasting_level": coffee.get('roasting_level', 'Unknown'),
                "grinding_level": coffee.get('grinding_level', 'Unknown'),
                "brewing_ratio": coffee.get('brewing_ratio', 'Unknown'),
                "tasting_notes": coffee.get('tasting_notes', 'Unknown')
            } for coffee in selected_coffees]}
            
            Your task is to provide a helpful and educational response to the user's query using 
            ONLY the experimental data provided above. 
            
            CRITICAL REQUIREMENTS:
            - Base your response ONLY on the selected coffee experiments provided
            - ALWAYS include specific database IDs when referencing experiments
            - Use the brewing_ratio and tasting_notes from the experimental data
            - Provide reasoning based on the actual experimental results
            - Be friendly, knowledgeable, and helpful
            - NEVER make up or fabricate coffee data, experiment IDs, or brewing results
            
            Format your response to be engaging and educational while staying grounded in the 
            real experimental data provided.
            """,
            expected_output="A helpful and educational response about coffee using the selected experimental data",
            agent=self.agent
        )
        
        # Execute second task
        crew2 = Crew(
            agents=[self.agent],
            tasks=[task2],
            process=Process.sequential,
            verbose=True
        )
        
        result2 = crew2.kickoff()
        
        # Log the second task result
        self._log_matching_coffees("TASK2_RESPONSE", {"selected_coffees": len(selected_coffees)}, selected_coffees, user_query=f"Task 2: {message}")
        
        return result2
    
    def close(self):
        """Close the coffee database connection."""
        print(f"Session ended. Log saved to: {self.log_filename}")
        self.coffee_manager.close()


# Example usage
if __name__ == "__main__":
    # Initialize Sammy (you'll need to set OPENROUTER_API_KEY environment variable)
    try:
        sammy = SammyTheSpartanBarista()
        
        # Example: Get coffee recommendations
        preferences = {"roasting_level": "Medium", "grinding_level": "Medium"}
        recommendations = sammy.get_coffee_recommendation(preferences)
        print("Coffee Recommendations:")
        print(recommendations)
        
        # Example: Chat with Sammy
        response = sammy.chat_with_sammy("What's the difference between light and dark roast coffee?")
        print("\nSammy's Response:")
        print(response)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your OPENROUTER_API_KEY environment variable")
    
    finally:
        if 'sammy' in locals():
            sammy.close()
