import streamlit as st
import asyncio
import sys
from io import StringIO
from day2 import run_shipping_workflow

# Initialize session state
if 'approval_required' not in st.session_state:
    st.session_state.approval_required = False
if 'approval_request' not in st.session_state:
    st.session_state.approval_request = None
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'auto_approve' not in st.session_state:
    st.session_state.auto_approve = True

# Set page config
st.set_page_config(
    page_title="Shipping Coordinator",
    page_icon="🚢",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea {
        font-size: 16px;
        min-height: 100px;
    }
    .stMarkdown h1 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for app info and settings
with st.sidebar:
    st.title("Shipping Coordinator 🚢")
    st.markdown("""
    ### How to use:
    1. Enter your shipping request in the text area
    2. For large orders (>5 containers), the system will ask for approval
    3. Check the console output for detailed workflow
    """)
    
    st.markdown("---")
    st.markdown("### Settings")
    auto_approve = st.checkbox("Auto-approve large orders", value=True, 
                             help="When checked, large orders will be automatically approved")

# ... (previous imports and setup remain the same)

# ... (previous imports and setup remain the same)

async def process_approval():
    with st.spinner("Processing your approval..."):
        output_buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output_buffer
        
        try:
            # Print the shipping request details
            print(f"\n=== Processing Order ===")
            print(f"Request: {st.session_state.approval_request}")
            print(f"Approval Status: {'Approved' if st.session_state.auto_approve else 'Rejected'}")
            
            # Run the workflow with the approval decision
            await run_shipping_workflow(
                st.session_state.approval_request, 
                auto_approve=st.session_state.auto_approve
            )
            
            output_text = output_buffer.getvalue()
            return output_text
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            output_buffer.close()
            sys.stdout = old_stdout

def main():
    st.title("Shipping Order System")
    
    # User input
    st.markdown("### Enter Your Shipping Request")
    st.markdown("Example: \"Ship 10 containers to Rotterdam\"")
    
    # Text input for shipping request
    user_input = st.text_area("Your request:", 
                            placeholder="Ship [number] containers to [destination]",
                            value=st.session_state.user_input,
                            label_visibility="collapsed")
    
    # Submit button
    if st.button("Submit Order", type="primary") and not st.session_state.approval_required:
        if user_input.strip():
            st.session_state.processing_done = False
            st.session_state.user_input = user_input
            with st.spinner("Processing your order..."):
                # Create a placeholder for the output
                output = st.empty()
                
                # Create a container for the output
                with output.container():
                    st.markdown("### Order Processing")
                    st.markdown("---")
                    
                    # Create a StringIO object to capture output
                    output_buffer = StringIO()
                    old_stdout = sys.stdout
                    sys.stdout = output_buffer
                    
                    try:
                        # Run the async function
                        asyncio.run(run_shipping_workflow(user_input, auto_approve=auto_approve))
                        
                        # Get the output from the buffer
                        output_text = output_buffer.getvalue()
                        output_buffer.close()
                        sys.stdout = old_stdout
                        
                        # Display the output
                        st.text_area("Processing Log:", 
                                   value=output_text,
                                   height=300)
                        
                        st.session_state.processing_done = True
                        
                        # Check if approval is needed
                        if "Pausing for approval" in output_text:
                            st.session_state.approval_required = True
                            st.session_state.approval_request = user_input
                            st.rerun()
                            
                    except Exception as e:
                        # Restore stdout in case of error
                        sys.stdout = old_stdout
                        st.error(f"An error occurred: {str(e)}")
                    
                    if st.session_state.processing_done and not st.session_state.approval_required:
                        st.success("Order processing complete!")
                        st.session_state.approval_request = None
        else:
            st.warning("Please enter a shipping request")

    # Approval buttons
    if st.session_state.approval_required and st.session_state.approval_request:
        st.warning("Approval Required")
        st.write(f"Order request: {st.session_state.approval_request}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve", type="primary"):
                st.session_state.approval_required = False
                st.session_state.auto_approve = True
                st.session_state.approval_decision = True
                st.rerun()
        
        with col2:
            if st.button("❌ Reject", type="secondary"):
                st.session_state.approval_required = False
                st.session_state.auto_approve = False
                st.session_state.approval_decision = False
                st.rerun()

    # Handle the approval response
    if hasattr(st.session_state, 'approval_decision'):
        with st.spinner("Processing your approval..."):
            output_buffer = StringIO()
            old_stdout = sys.stdout
            sys.stdout = output_buffer
            
            try:
                # Print the shipping request details
                print(f"\n=== Processing Order ===")
                print(f"Request: {st.session_state.approval_request}")
                print(f"Approval Status: {'Approved' if st.session_state.auto_approve else 'Rejected'}")
                
                # Run the workflow with the approval decision
                asyncio.run(run_shipping_workflow(
                    st.session_state.approval_request, 
                    auto_approve=st.session_state.auto_approve
                ))
                
                output_text = output_buffer.getvalue()
                output_buffer.close()
                sys.stdout = old_stdout
                
                # Display the final output
                st.markdown("### Order Processing Complete")
                st.markdown("---")
                st.text_area("Processing Log:", 
                           value=output_text,
                           height=300)
                
                st.success("Order processing complete!")
                
                # Clean up
                if 'approval_decision' in st.session_state:
                    del st.session_state.approval_decision
                st.session_state.approval_request = None
                
            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    