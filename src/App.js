import './App.css';

function App() {
    return (
        <div className="App">
            <div className="form_box">
                <div className="left_part">
                    <div className="content_left">
                        <h3>Welcome back</h3>

                        <p>Already have an account?, click below <br/> to continue managing your files</p>

                        <a href={"#"}>Sign In</a>
                    </div>
                </div>

                <div className="right_part">
                    <h2>Create Account</h2>

                    <form action="">
                        <div className="form-group">
                            <label htmlFor="name"><i className='bx bx-user'></i></label>
                            <input type="text" id={"name"} placeholder={"Username"}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="email"><i className='bx bx-envelope'></i></label>
                            <input type="email" id={"email"} placeholder={"Email"}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="contact"><i className='bx bx-phone'></i></label>
                            <input type="text" id={"contact"} placeholder={"Contact"}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="pwd"><i className='bx bx-lock-alt'></i></label>
                            <input type="text" id={"pwd"} placeholder={"Password"}/>
                        </div>
                        <button>Sign Up</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default App;
