import requests
import streamlit as st
import os
from dotenv import load_dotenv


def search_coop_opportunities():
    # Load environment variables
    load_dotenv()
    API_URL = os.getenv('API_URL', 'http://localhost:4000')

    st.title("Search for Co-op Opportunities")

    # Display API connection status
    try:
        requests.get(f"{API_URL}/", timeout=5)
        st.success("✅ Connected to API server")
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to API server. Please ensure the backend server is running on " + API_URL)
        st.info("To fix this:\n1. Make sure the Flask backend is running\n2. Verify the API_URL in your .env file\n3. Check if the port 4000 is available")
        return

    # Input fields for user query
    keyword = st.text_input("Enter a keyword (e.g., 'Data Analyst')", "")
    location = st.text_input("Enter a location (e.g., 'Boston')", "")

    # Search button
    if st.button("Search"):
        # Update URL to use environment variable
        url = f"{API_URL}/positions"

        # Query parameters
        params = {}
        if keyword:
            params["PositionTitle"] = keyword
        if location:
            params["Location"] = location

        # Make the GET request
        try:
            response = requests.get(url, params=params, timeout=10)  # 10-second timeout
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse and display results
            results = response.json()
            if results:
                st.write("### Results:")
                for result in results:
                    st.write(f"**Title:** {result.get('PositionTitle', 'N/A')}")
                    st.write(f"**Location:** {result.get('Location', 'N/A')}")
                    st.write(f"**Salary Range:** {result.get('SalaryRange', 'N/A')}")
                    st.write(f"**Type:** {result.get('PositionType', 'N/A')}")
                    st.write("---")
            else:
                st.warning("No results found. Please try with different filters.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error("Error parsing the response. Please check the server output.")


if __name__ == "__main__":
    search_coop_opportunities()