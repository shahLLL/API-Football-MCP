import logging
from mcp.server.fastmcp import FastMCP
from typing import Any
from api_requests import make_api_request

# Configure logger
logging.basicConfig(level=logging.INFO)
logging.info("API-Football Server Running")

# Initialize FastMCP server
mcp = FastMCP("footy")

# MCP Tools
@mcp.tool()
async def get_squad(team_name: str) -> list[dict[str, Any]] | None:
    team_url = "https://v3.football.api-sports.io/teams?name={}".format(team_name)
    team_response = await make_api_request(team_url)
    if not team_response:
        return None
    team_id = team_response['response'][0]['team']['id']

    squad_url = "https://v3.football.api-sports.io/players/squads?team={}".format(team_id)
    squad_response = await make_api_request(squad_url)
    if not squad_response:
        return None
    logging.info(squad_response['response'][0]['players'])
    return squad_response['response'][0]['players']

# MCP Prompts
@mcp.prompt()
def show_squad(team_name: str) -> str:
    """
    Instructions to display a team's squad in a formatted table.
    """
    return (
        f"You are a football data analyst. Your goal is to present the {team_name} "
        "squad in a professional, easy-to-read dashboard format.\n\n"
        "STEPS:\n"
        "1. Fetch the roster data for {team_name} using the football tool.\n"
        "2. Organize the players into distinct sections by Position: "
        "Goalkeepers, Defenders, Midfielders, and Attackers.\n"
        "3. FORMATTING:\n"
        "   - Use a Markdown table for each position group.\n"
        "   - Column headers: | 👤 | Name | # | Age |\n"
        "   - In the first column (👤), use a consistent emoji based on position: "
        "🧤 for GK, 🛡️ for DEF, ⚙️ for MID, ⚡ for ATK.\n"
        "4. STYLING:\n"
        "   - **Bold** all player names.\n"
        "   - Center-align the Number (#) and Age columns.\n"
        "5. SUMMARY: At the bottom, add a brief note on the 'Average Squad Age' "
        "based on the data retrieved."
    )

# Main
def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()