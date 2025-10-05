"""
Educational logging utility for demo purposes.
Shows detailed, colorful logs explaining what's happening at each step.
"""
import sys


class Color:
    """ANSI color codes."""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


class EducationalLogger:
    """Logger that explains the AI orchestration process."""
    
    @staticmethod
    def log_step(emoji: str, title: str, description: str, details: dict = None):
        """Log a major step in the workflow."""
        print(f"\n{Color.BOLD}{Color.CYAN}{emoji} {title}{Color.RESET}")
        print(f"{Color.DIM}   → {description}{Color.RESET}")
        
        if details:
            for key, value in details.items():
                print(f"{Color.WHITE}   • {key}: {Color.GREEN}{value}{Color.RESET}")
    
    @staticmethod
    def log_agent(agent_name: str, action: str):
        """Log an agent action."""
        print(f"{Color.MAGENTA}🤖 {agent_name}{Color.RESET} {Color.DIM}is {action}...{Color.RESET}")
    
    @staticmethod
    def log_result(result: str, success: bool = True):
        """Log a result."""
        color = Color.GREEN if success else Color.RED
        icon = "✅" if success else "❌"
        print(f"{color}   {icon} {result}{Color.RESET}")
    
    @staticmethod
    def log_inference(parameter: str, value: str, reason: str):
        """Log parameter inference."""
        print(f"{Color.YELLOW}   🔮 Inferred {parameter} = '{value}'{Color.RESET}")
        print(f"{Color.DIM}      Reason: {reason}{Color.RESET}")
    
    @staticmethod
    def log_database(action: str, table: str, details: str = ""):
        """Log database operation."""
        print(f"{Color.BLUE}   💾 Database: {action} → {table}{Color.RESET}", end="")
        if details:
            print(f" {Color.DIM}({details}){Color.RESET}")
        else:
            print()
    
    @staticmethod
    def log_context(context_type: str, info: str):
        """Log context usage."""
        print(f"{Color.CYAN}   📚 Using context: {context_type} - {info}{Color.RESET}")
    
    @staticmethod
    def log_validation(field: str, status: str, message: str = ""):
        """Log validation."""
        icon = "✓" if status == "valid" else "⚠"
        color = Color.GREEN if status == "valid" else Color.YELLOW
        print(f"{color}   {icon} Validating {field}: {status}{Color.RESET}", end="")
        if message:
            print(f" {Color.DIM}- {message}{Color.RESET}")
        else:
            print()
    
    @staticmethod
    def log_tool_call(tool_name: str, endpoint: str):
        """Log tool API call."""
        print(f"\n{Color.BOLD}{Color.MAGENTA}🔧 Calling Educational Tool:{Color.RESET}")
        print(f"{Color.WHITE}   Tool: {tool_name}{Color.RESET}")
        print(f"{Color.DIM}   Endpoint: {endpoint}{Color.RESET}")
    
    @staticmethod
    def log_separator():
        """Print a separator line."""
        print(f"{Color.DIM}{'─' * 80}{Color.RESET}")


# Global instance
edu_logger = EducationalLogger()
