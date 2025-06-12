import streamlit as st
import logging

# Configure logging
logging.basicConfig(
    filename="retirement_calculator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to calculate total retirement savings needed
def calculate_retirement_savings(hme, mle, go, ve, gm, fme, ee, hce, a, r, le, i, r_rate):
    try:
        # Calculate total annual expenses
        annual_expenses = 12 * (hme + mle + go + fme + hce) + ve + gm + ee

        # Adjust for inflation from now to retirement
        years_to_retirement = r - a
        inflation_adjusted_expenses = annual_expenses * ((1 + i) ** years_to_retirement)

        # Number of years in retirement
        years_in_retirement = le - r

        # Real return rate (investment return adjusted for inflation)
        real_return_rate = r_rate - i

        # Ensure that real return rate is positive
        if real_return_rate <= 0:
            st.error("The real return rate must be greater than 0. Adjust inflation or return rates.")
            logging.error("Invalid real return rate: r_rate - i <= 0")
            return None

        # Formula for total savings required at retirement
        total_savings = (inflation_adjusted_expenses / real_return_rate) * (
            1 - (1 / ((1 + real_return_rate) ** years_in_retirement))
        )

        return total_savings

    except Exception as e:
        st.error("An error occurred during the calculation. Please check your inputs.")
        logging.error(f"Error during calculation: {e}")
        return None


# Streamlit App
def main():
    # Add a sidebar for navigation and branding
    st.sidebar.title("Retirement Calculator")
    st.sidebar.info(
        """
        This app helps you estimate how much money you need to save for retirement
        based on your lifestyle and financial assumptions.  
        """
    )

    # App title and description
    st.title("💼 Retirement Savings Calculator")
    st.write("Plan your retirement with confidence. Enter your details below to get started.")

    # Inputs for monthly and annual expenses
    st.header("🛠️ Expenses")
    hme = st.number_input("House Monthly Expenses (Rent, Mortgage, Maintenance, Utilities, Insurance)", min_value=0, value=7000)
    mle = st.number_input("Monthly Living Expenses (Food, Groceries)", min_value=0, value=2000)
    go = st.number_input("Going Out Monthly Expenses (Dinner, Drinks, Socialization)", min_value=0, value=1500)
    ve = st.number_input("Vacation Expenses Per Year", min_value=0, value=10000)
    gm = st.number_input("Golf Membership and Outing Expenses Per Year", min_value=0, value=25000)
    fme = st.number_input("Family Monthly Expenses (Gifts for Kids, Grandkids)", min_value=0, value=500)
    ee = st.number_input("Emergency Expenses Per Year", min_value=0, value=5000)
    hce = st.number_input("Monthly Healthcare Expenses", min_value=0, value=2000)

    # Inputs for personal details
    st.header("👤 Personal Details")
    a = st.number_input("Current Age", min_value=0, value=50)
    r = st.number_input("Retirement Age", min_value=0, value=60)
    le = st.number_input("Life Expectancy (Age)", min_value=0, value=85)

    # Error checking for retirement age and life expectancy
    if r <= a:
        st.error("Retirement age must be greater than current age.")
        logging.error("Retirement age is less than or equal to current age.")
        return
    if le <= r:
        st.error("Life expectancy must be greater than retirement age.")
        logging.error("Life expectancy is less than or equal to retirement age.")
        return

    # Inputs for financial assumptions
    st.header("📊 Financial Assumptions")
    i = st.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=10.0, value=3.5) / 100
    r_rate = st.slider("Annual Investment Return Rate (%)", min_value=0.0, max_value=10.0, value=5.0) / 100

    # Calculate the retirement savings
    if st.button("💰 Calculate"):
        st.info("Calculating your retirement savings...")
        total_savings = calculate_retirement_savings(hme, mle, go, ve, gm, fme, ee, hce, a, r, le, i, r_rate)
        
        if total_savings is not None:
            st.success(f"💵 Total Retirement Savings Needed: ${total_savings:,.2f}")
            logging.info(f"Calculation successful: Total Savings = ${total_savings:,.2f}")
        else:
            logging.warning("Calculation returned None due to input issues.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        **Professional Retirement Calculator**  
        Built with 💻 by [Rajesh Arora].  
        For feedback or support, contact us at [rajesh.arora@gmail.com].
        """
    )


# Run the app
if __name__ == "__main__":
    main()