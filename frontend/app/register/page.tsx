
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { register } from "@/lib/api";
import Link from "next/link";

const inputStyle = {
  width: "100%",
  padding: "12px 16px",
  borderRadius: 10,
  border: "2px solid #e5e7eb",
  fontSize: 15,
  outline: "none",
  boxSizing: "border-box" as const,
  fontFamily: "inherit",
  transition: "border-color 0.2s",
};

const labelStyle = {
  display: "block",
  fontWeight: 600 as const,
  color: "#374151",
  marginBottom: 6,
  fontSize: 14,
};

export default function RegisterPage() {
  const [form, setForm] = useState({
    name: "",
    mobile_number: "",
    email: "",
    password: "",
    school: "",
    student_class: "",
    father_name: "",
    mother_name: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    // Allow digits only and limit the Indian mobile number to 10 digits.
    const updatedValue =
      name === "mobile_number"
        ? value.replace(/\D/g, "").slice(0, 10)
        : value;

    setForm((previous) => ({
      ...previous,
      [name]: updatedValue,
    }));
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!/^[6-9]\d{9}$/.test(form.mobile_number)) {
      setError("Enter a valid 10-digit Indian mobile number.");
      return;
    }

    setLoading(true);

    try {
      const res = await register(form);

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("user_name", res.data.name || form.name);
      localStorage.setItem("user_email", res.data.email || form.email);

      router.push("/test");
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Registration failed."
      );
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    {
      name: "name",
      label: "Full Name *",
      type: "text",
      placeholder: "Enter your full name",
      span: 2,
      required: true,
    },
    {
      name: "mobile_number",
      label: "Student Mobile Number *",
      type: "tel",
      placeholder: "Enter 10-digit mobile number",
      span: 2,
      required: true,
    },
    {
      name: "email",
      label: "Email *",
      type: "email",
      placeholder: "Enter your email",
      span: 1,
      required: true,
    },
    {
      name: "password",
      label: "Password *",
      type: "password",
      placeholder: "Min 8 characters",
      span: 1,
      required: true,
    },
    {
      name: "school",
      label: "School Name *",
      type: "text",
      placeholder: "Enter your school name",
      span: 2,
      required: true,
    },
    {
      name: "student_class",
      label: "Class *",
      type: "text",
      placeholder: "e.g. XII, 10th",
      span: 1,
      required: true,
    },
    {
      name: "father_name",
      label: "Father's Name",
      type: "text",
      placeholder: "Enter father's name",
      span: 1,
      required: false,
    },
    {
      name: "mother_name",
      label: "Mother's Name",
      type: "text",
      placeholder: "Enter mother's name",
      span: 2,
      required: false,
    },
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg,#667eea 0%,#764ba2 100%)",
        fontFamily: "'Segoe UI',sans-serif",
        padding: 20,
      }}
    >
      <div
        style={{
          background: "white",
          borderRadius: 24,
          padding: "48px 44px",
          width: "100%",
          maxWidth: 560,
          boxShadow: "0 25px 60px rgba(0,0,0,0.2)",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <img
            src="/logo.png"
            alt="Knowletive"
            style={{
              height: 80,
              objectFit: "contain",
              margin: "0 auto 16px",
              display: "block",
            }}
          />

          <h2
            style={{
              fontSize: 26,
              fontWeight: 700,
              color: "#1a1a2e",
              margin: "0 0 6px",
            }}
          >
            Create Account
          </h2>

          <p style={{ color: "#888", fontSize: 14, margin: 0 }}>
            Register to take the psychometric assessment
          </p>
        </div>

        {error && (
          <div
            role="alert"
            style={{
              background: "#fff0f0",
              border: "1px solid #fca5a5",
              color: "#dc2626",
              padding: "12px 16px",
              borderRadius: 10,
              marginBottom: 20,
              fontSize: 14,
            }}
          >
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleRegister}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "minmax(0, 1fr) minmax(0, 1fr)",
              gap: 16,
            }}
          >
            {fields.map((f) => (
              <div
                key={f.name}
                style={{ gridColumn: `span ${f.span}`, minWidth: 0 }}
              >
                <label htmlFor={f.name} style={labelStyle}>
                  {f.label}
                </label>

                <input
                  id={f.name}
                  type={f.type}
                  name={f.name}
                  value={form[f.name as keyof typeof form]}
                  onChange={handleChange}
                  placeholder={f.placeholder}
                  required={f.required}
                  autoComplete={
                    f.name === "mobile_number"
                      ? "tel-national"
                      : f.name === "name"
                      ? "name"
                      : f.name === "email"
                      ? "email"
                      : f.name === "password"
                      ? "new-password"
                      : "off"
                  }
                  inputMode={
                    f.name === "mobile_number" ? "numeric" : undefined
                  }
                  maxLength={f.name === "mobile_number" ? 10 : undefined}
                  pattern={
                    f.name === "mobile_number"
                      ? "[6-9][0-9]{9}"
                      : undefined
                  }
                  title={
                    f.name === "mobile_number"
                      ? "Enter a valid 10-digit Indian mobile number."
                      : undefined
                  }
                  style={inputStyle}
                  onFocus={(e) => {
                    e.currentTarget.style.borderColor = "#667eea";
                  }}
                  onBlur={(e) => {
                    e.currentTarget.style.borderColor = "#e5e7eb";
                  }}
                />
              </div>
            ))}
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: 14,
              marginTop: 24,
              background: loading
                ? "#a78bfa"
                : "linear-gradient(135deg,#667eea,#764ba2)",
              color: "white",
              border: "none",
              borderRadius: 10,
              fontSize: 16,
              fontWeight: 700,
              cursor: loading ? "not-allowed" : "pointer",
              fontFamily: "inherit",
            }}
          >
            {loading
              ? "Creating account..."
              : "Create Account & Start Test →"}
          </button>
        </form>

        <p
          style={{
            textAlign: "center",
            color: "#888",
            marginTop: 20,
            fontSize: 14,
          }}
        >
          Already have an account?{" "}
          <Link
            href="/"
            style={{
              color: "#667eea",
              fontWeight: 700,
              textDecoration: "none",
            }}
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
